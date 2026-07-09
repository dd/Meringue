import warnings
import zlib
from functools import cached_property
from functools import wraps

from django.db import connections


def _check_postgresql(using: str) -> bool:
    """
    Check whether the selected DB engine is PostgreSQL.
    """

    return connections[using].vendor == "postgresql"


def _int_lock_id(lock_id: int | str, namespace_id: int | str | None = None) -> int:
    """
    Returns the integer form of `lock_id`, applying CRC32 hash if it's a string.
    """

    if isinstance(lock_id, int):
        return lock_id

    unsigned = zlib.crc32(lock_id.encode("utf-8")) & 0xFFFFFFFF

    if namespace_id is not None:
        return unsigned - 0x80000000

    return unsigned


def _int_namespace_id(namespace_id: int | str | None) -> int | None:
    """
    Returns the integer form of `namespace_id`, applying CRC32 hash if it's a string.
    """

    if namespace_id is None:
        return None

    if isinstance(namespace_id, int):
        return namespace_id

    unsigned = zlib.crc32(namespace_id.encode("utf-8")) & 0xFFFFFFFF
    return unsigned - 0x80000000


def _advisory_lock_args(lock_id: int | str, namespace_id: int | str | None) -> list[int]:
    """
    Returns PostgreSQL advisory lock arguments for single-key or namespace-key signatures.
    """

    if namespace_id is None:
        return [_int_lock_id(lock_id)]

    namespace_arg = _int_namespace_id(namespace_id)
    if namespace_arg is None:
        msg = "namespace_id cannot be None when using two advisory lock arguments."
        raise ValueError(msg)

    return [namespace_arg, _int_lock_id(lock_id, namespace_id)]


class PgAdvisoryLock:
    """
    PostgreSQL advisory lock for Django projects.

    This utility provides a context manager and decorator for safely acquiring PostgreSQL advisory
    locks based on either a single integer key or a (namespace, key) pair.

    !!! info "supports both signatures"
        - `pg_advisory_lock(key)`            — if only `lock_id` is provided
        - `pg_advisory_lock(namespace, key)` — if `namespace_id` is also provided

    !!! warning
        If the database is not PostgreSQL, the lock will **not** be applied.
        A warning will be issued, but the function or block will still execute normally.

    !!! warning
        If you pass strings for lock_id or namespace_id, they will be hashed to 32-bit signed ints
        using CRC32. Locks persist until manually released or until the DB session ends.

    Examples:
        ```py title="As context manager"
        with PgAdvisoryLock(12345, namespace_id="transaction"):
            ...
        ```

        ```py title="As decorator"
        @PgAdvisoryLock(12345)
        def process_transfer():
            ...
        ```

        ```py title="Classic"
        adv_lock = PgAdvisoryLock(12345)
        adv_lock.lock()
        ...
        adv_lock.unlock()
        ```
    """

    def __init__(
        self,
        lock_id: int | str,
        namespace_id: int | str | None = None,
        using: str = "default",
    ):
        """
        Args:
            lock_id: Unique identifier for the resource to be locked.
                Strings are hashed to a 32-bit signed integer.
            namespace_id: Optional namespace (e.g. table name or resource type)
                to avoid key collisions. Also hashed if passed as a string.
            using: Django database alias.
        """

        self.lock_id = lock_id
        self.namespace_id = namespace_id
        self.db_name = using
        self.is_postgresql = self._check_postgresql()
        self.__stacklevel = 2

    def __enter__(self):
        self.__stacklevel += 1
        self.lock()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.unlock()
        return False

    def __call__(self, func):
        self.__stacklevel += 1

        @wraps(func)
        def wrapped(*args, **kwargs):
            with self:
                return func(*args, **kwargs)

        return wrapped

    def _check_postgresql(self) -> bool:
        """
        Check whether the current DB engine is PostgreSQL.
        """

        return _check_postgresql(self.db_name)

    @cached_property
    def int_lock_id(self) -> int:
        """
        Returns the integer form of `lock_id`, applying CRC32 hash if it's a string.

        Returns:
            32-bit signed integer key for pg_advisory_lock.
        """

        return _int_lock_id(self.lock_id, self.namespace_id)

    @cached_property
    def int_namespace_id(self) -> int | None:
        """
        Returns the integer form of `namespace_id`, applying CRC32 hash if it's a string.

        Returns:
            Signed 32-bit integer or None if namespace is not set.
        """

        return _int_namespace_id(self.namespace_id)

    def lock(self) -> None:
        """
        Acquires the advisory lock.
        """

        if not self.is_postgresql:
            msg = "pg_advisory_lock is only supported with PostgreSQL databases."
            warnings.warn(msg, UserWarning, stacklevel=self.__stacklevel)
            return

        if self.namespace_id is None:
            sql = "SELECT pg_advisory_lock(%s)"
            args = [self.int_lock_id]
        else:
            sql = "SELECT pg_advisory_lock(%s, %s)"
            args = [self.int_namespace_id, self.int_lock_id]

        with connections[self.db_name].cursor() as cursor:
            cursor.execute(sql, args)

    def unlock(self) -> None:
        """
        Releases the advisory lock.
        """

        if not self.is_postgresql:
            return

        if self.namespace_id is None:
            sql = "SELECT pg_advisory_unlock(%s)"
            args = [self.int_lock_id]
        else:
            sql = "SELECT pg_advisory_unlock(%s, %s)"
            args = [self.int_namespace_id, self.int_lock_id]

        with connections[self.db_name].cursor() as cursor:
            cursor.execute(sql, args)


def pg_advisory_xact_lock(
    lock_id: int | str,
    namespace_id: int | str | None = None,
    using: str = "default",
) -> None:
    """
    PostgreSQL transaction-level advisory lock for Django projects.

    This function uses the same key handling as [PgAdvisoryLock][meringue.core.db.PgAdvisoryLock],
    but calls PostgreSQL's `pg_advisory_xact_lock` functions. Transaction-level advisory locks are
    released automatically at the end of the current transaction and cannot be released manually.

    !!! info "supports both signatures"
        - `pg_advisory_xact_lock(key)`            — if only `lock_id` is provided
        - `pg_advisory_xact_lock(namespace, key)` — if `namespace_id` is also provided

    !!! warning
        In Django autocommit mode this lock is released at the end of the SQL statement. Wrap usage
        in `transaction.atomic()` when the lock must be held for a block of application code.

    Examples:
        ```py
        from django.db import transaction

        with transaction.atomic():
            pg_advisory_xact_lock(12345, namespace_id="transfer")
            ...
        ```
    """

    if not _check_postgresql(using):
        msg = "pg_advisory_xact_lock is only supported with PostgreSQL databases."
        warnings.warn(msg, UserWarning, stacklevel=2)
        return

    connection = connections[using]
    if connection.get_autocommit() and not connection.in_atomic_block:
        msg = (
            "pg_advisory_xact_lock is being used in autocommit mode. "
            "Wrap usage in transaction.atomic() to hold the lock for application code."
        )
        warnings.warn(msg, UserWarning, stacklevel=2)

    if namespace_id is None:
        sql = "SELECT pg_advisory_xact_lock(%s)"
    else:
        sql = "SELECT pg_advisory_xact_lock(%s, %s)"

    args = _advisory_lock_args(lock_id, namespace_id)

    with connection.cursor() as cursor:
        cursor.execute(sql, args)
