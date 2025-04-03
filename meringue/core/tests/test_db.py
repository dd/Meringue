from unittest import mock

import pytest

from meringue.core.db import PgAdvisoryLock


@pytest.mark.parametrize(
    "lock_id, expected",
    [
        ("test_lock_id", 1596780821),
        (42, 42),
    ],
)
def test_int_lock_id(lock_id, expected):
    """
    Проверка расчёта lock ID
    """

    lock = PgAdvisoryLock(lock_id)
    assert lock.int_lock_id == expected


@pytest.mark.parametrize(
    "lock_id, expected",
    [
        ("test_lock_id", -550702827),
        (42, 42),
    ],
)
def test_int_lock_id_with_namespace(lock_id, expected):
    """
    Проверка расчёта lock ID при указаном namespace ID

    Если задавать namespace то расчитывая lock ID происходит смещение чтобы вписаться в int
    postgresql
    """

    lock = PgAdvisoryLock(lock_id, 42)
    assert lock.int_lock_id == expected


@pytest.mark.parametrize(
    "namespace_id, expected",
    [
        ("test_namespace_id", -202238029),
        (42, 42),
        (None, None),
    ],
)
def test_int_namespace_id(namespace_id, expected):
    """
    Проверка расчёта namespace ID
    """

    lock = PgAdvisoryLock(None, namespace_id)
    assert lock.int_namespace_id == expected


@pytest.mark.parametrize(
    "lock_id, namespace_id, sql, args",
    [
        (42, None, "SELECT pg_advisory_lock(%s)", [42]),
        (42, 42, "SELECT pg_advisory_lock(%s, %s)", [42, 42]),
    ],
)
@pytest.mark.django_db
def test_lock_calls_cursor_execute_single_key(lock_id, namespace_id, sql, args):
    """
    Проверка выполняемых sql запросов при вызове lock()
    """

    lock = PgAdvisoryLock(lock_id, namespace_id)
    lock.is_postgresql = True  # пропускаем проверку

    with mock.patch("django.db.backends.utils.CursorWrapper.execute") as mock_execute:
        lock.lock()

    # mock_execute.assert_called_once_with(sql, args)
    mock_execute.assert_called_once()
    called_args = mock_execute.call_args
    assert called_args[0][0] == sql
    assert called_args[0][1] == args


@pytest.mark.parametrize(
    "lock_id, namespace_id, sql, args",
    [
        (42, None, "SELECT pg_advisory_unlock(%s)", [42]),
        (42, 42, "SELECT pg_advisory_unlock(%s, %s)", [42, 42]),
    ],
)
@pytest.mark.django_db
def test_unlock_calls_cursor_execute_single_key(lock_id, namespace_id, sql, args):
    """
    Проверка выполняемых sql запросов при вызове unlock()
    """

    lock = PgAdvisoryLock(lock_id, namespace_id)
    lock.is_postgresql = True  # пропускаем проверку

    with mock.patch("django.db.backends.utils.CursorWrapper.execute") as mock_execute:
        lock.unlock()

    mock_execute.assert_called_once_with(sql, args)


def test_warn_if_not_postgresql():
    """
    Проверка что выводится сообщение пользователю
    """

    lock = PgAdvisoryLock("test")
    lock.is_postgresql = False

    with pytest.warns(
        UserWarning,
        match="pg_advisory_lock is only supported with PostgreSQL databases.",
    ):
        lock.lock()


def test_skip_lock_with_not_postgresql_db():
    """
    Проверка что если база не postgresql то lock не вызывается
    """

    lock = PgAdvisoryLock("test")
    lock.is_postgresql = False

    with mock.patch("django.db.backends.utils.CursorWrapper.execute") as mock_execute:
        lock.lock()

    mock_execute.assert_not_called()


def test_skip_unlock_with_not_postgresql_db():
    """
    Проверка что если база не postgresql то unlock не вызывается
    """

    lock = PgAdvisoryLock("test")
    lock.is_postgresql = False

    with mock.patch("django.db.backends.utils.CursorWrapper.execute") as mock_execute:
        lock.unlock()

    mock_execute.assert_not_called()


def test_use_as_with():
    """
    Проверяем что утилита используется как контекстный менеджер
    """

    with (
        mock.patch.object(PgAdvisoryLock, "lock") as mock_lock,
        mock.patch.object(PgAdvisoryLock, "unlock") as mock_unlock,
    ):

        with PgAdvisoryLock("test"):
            mock_lock.assert_called_once()
            mock_unlock.assert_not_called()

        mock_lock.assert_called_once()
        mock_unlock.assert_called_once()


def test_use_as_decorator():
    """
    Проверяем что утилита используется как декоратор
    """

    with (
        mock.patch.object(PgAdvisoryLock, "lock") as mock_lock,
        mock.patch.object(PgAdvisoryLock, "unlock") as mock_unlock,
    ):

        @PgAdvisoryLock("test")
        def test_fn():
            mock_lock.assert_called_once()
            mock_unlock.assert_not_called()

        test_fn()
        mock_lock.assert_called_once()
        mock_unlock.assert_called_once()
