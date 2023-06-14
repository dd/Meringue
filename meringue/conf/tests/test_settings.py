from unittest.mock import patch

from django.test import override_settings

from meringue.conf import Settings


def test__all_good_without_user_setting():
    """
    We check that if there is no parameter in the django settings, the Meringue settings are loaded
    successfully
    """
    foo_settings = Settings("TEST_MERINGUE", {}, {}, [])
    assert getattr(foo_settings, "TEST_MERINGUE", None) is None


def test__import_properties():
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
def test__cache_properties(getter):
    """
    We check that when the property is accessed again, the value is taken from the cache, and not
    parsed again
    """
    foo_settings = Settings("TEST_MERINGUE", {"TEST_PROP": "value"}, {}, [])
    assert foo_settings.TEST_PROP == "value"
    assert foo_settings.TEST_PROP == "value"
    getter.assert_called_once_with(foo_settings, "TEST_PROP")


@override_settings(TEST_MERINGUE={"OVERRIDED_PROP": "value 2"})
def test__redefining():
    """
    Checking that override the property value by the user in the project settings works
    """
    foo_settings = Settings("TEST_MERINGUE", {"OVERRIDED_PROP": "value"}, {}, [])
    assert foo_settings.OVERRIDED_PROP == "value 2"
