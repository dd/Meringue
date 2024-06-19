import warnings
from functools import wraps

from django.conf import settings
from django.db import connections


class PgAdvisoryLock:
    """
    A context manager and decorator for using PostgreSQL advisory locks in Django.

    This class provides a way to use PostgreSQL advisory locks, ensuring that the lock
    is acquired and released correctly. It supports usage as both a context manager
    and a function decorator. The class also checks if the database is PostgreSQL and
    issues a warning if it is not.
    """

    def __init__(self, table: str, value: str, field: str = "id", using: str = "default"):
        """
        Attributes:
            table: The name of the table to query for the lock ID.
            value: The value to match in the field to retrieve the lock ID.
            field: The name of the field to query for the lock ID.
            using: The database alias to use.
        """

        self.table = table
        self.value = value
        self.field = field
        self.db_name = using
        self.is_postgresql = self._check_postgresql()

    def __enter__(self):
        self.lock()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.unlock()
        return False

    def __call__(self, func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            with self:
                return func(*args, **kwargs)

        return wrapped

    def _check_postgresql(self) -> bool:
        engine = settings.DATABASES[self.db_name]["ENGINE"]
        return "postgresql" in engine

    def lock(self) -> None:
        """
        Acquires the advisory lock.
        """

        if not self.is_postgresql:
            msg = "pg_advisory_lock is only supported with PostgreSQL databases."
            warnings.warn(msg, UserWarning, stacklevel=2)
            return

        sql = f"SELECT pg_advisory_lock({self.field}) FROM {self.table} WHERE {self.field} = %s"  # noqa: S608
        with connections[self.db_name].cursor() as cursor:
            cursor.execute(sql, [self.value])

    def unlock(self) -> None:
        """
        Releases the advisory lock.
        """

        if not self.is_postgresql:
            return

        sql = f"SELECT pg_advisory_unlock({self.field}) FROM {self.table} WHERE {self.field} = %s"  # noqa: S608
        with connections[self.db_name].cursor() as cursor:
            cursor.execute(sql, [self.value])
