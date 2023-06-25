from unittest.mock import patch

from django.conf import settings
from django.test import override_settings

import pytest

from meringue.conf import Settings


def test_all_good_without_user_setting():
    """
    We check that if there is no parameter in the django settings, the Meringue settings are loaded
    successfully
    """
    Settings("TEST_MERINGUE", {}, {}, [])
    assert getattr(settings, "TEST_MERINGUE", None) is None


def test_access_non_existent():
    """
    Accessing a non-existent parameter throws an error
    """
    foo_settings = Settings("TEST_MERINGUE", {}, {}, [])
    with pytest.raises(AttributeError, match="Invalid setting key: 'NOT_EXIST_PARAM'"):
        # the assert should not work, since the parameter access should return an error
        assert foo_settings.NOT_EXIST_PARAM


def test_deprecate_warnings():
    """
    Accessing a non-existent parameter throws an error
    """
    foo_settings = Settings(
        "TEST_MERINGUE",
        {"DEPRECATED_PARAM": None},
        {"DEPRECATED_PARAM": "Deprecated parameter for tests"},
        [],
    )
    with pytest.warns(DeprecationWarning, match="Deprecated parameter for tests"):
        assert foo_settings.DEPRECATED_PARAM is None


def test_default_config():
    """
    Checking that default ones are returned if not overridden
    """
    foo_settings = Settings("TEST_MERINGUE", {"OVERRIDED_PROP": "value"}, {}, [])
    assert foo_settings.OVERRIDED_PROP == "value"


@override_settings(TEST_MERINGUE={"OVERRIDED_PROP": "value 2"})
def test_configure():
    """
    Checking that override the property value by the user in the project settings works
    """
    foo_settings = Settings("TEST_MERINGUE", {"OVERRIDED_PROP": "value"}, {}, [])
    assert foo_settings.OVERRIDED_PROP == "value 2"


def test_import_properties():
    """
    Checking that the property import works successfully
    """
    foo_settings = Settings(
        "TEST_MERINGUE",
        {"IMPORTABLE_PROP": "meringue.conf.Settings"},
        {},
        ["IMPORTABLE_PROP"],
    )
    assert Settings == foo_settings.IMPORTABLE_PROP


@patch(
    "meringue.conf.Settings.__getattr__",
    autospec=True,
    side_effect=Settings.__getattr__,
)
def test_cache_properties(getter):
    """
    We check that when the property is accessed again, the value is taken from the cache, and not
    parsed again
    """
    foo_settings = Settings("TEST_MERINGUE", {"TEST_PROP": "value"}, {}, [])
    assert foo_settings.TEST_PROP
    assert foo_settings.TEST_PROP
    getter.assert_called_once_with(foo_settings, "TEST_PROP")


@patch(
    "meringue.conf.Settings.__getattr__",
    autospec=True,
    side_effect=Settings.__getattr__,
)
def test_reset_cache(getter):
    """
    Reset cache
    """
    foo_settings = Settings("TEST_MERINGUE", {"TEST_PROP": "value"}, {}, [])
    assert foo_settings.TEST_PROP
    foo_settings.reset()
    assert foo_settings.TEST_PROP
    assert getter.call_count == 2


@override_settings(TEST_MERINGUE={"OVERRIDED_PROP": "value 2"})
def test_redefining():
    """
    Checking that override the property value by the user in the project settings works
    """
    foo_settings = Settings("TEST_MERINGUE", {"OVERRIDED_PROP": "value"}, {}, [])
    assert foo_settings.OVERRIDED_PROP == "value 2"
