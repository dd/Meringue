from unittest.mock import patch

import pytest

from meringue.conf import import_dict
from meringue.conf import import_list
from meringue.conf import import_parameter


def test_import_list():
    """
    Verifying a successful list import.
    """
    value = [
        "meringue.conf.import_list",
    ]
    imported_list = import_list(value)
    assert imported_list == [import_list]


def test_import_list_wrong_type():
    """
    Checking for a data type error when importing a list.
    """
    msg = "`int` data type is not supported for import."
    with pytest.raises(TypeError, match=msg):
        import_list([1])


def test_import_list_non_existent():
    """
    Import error check for a list.
    """
    msg = "`meringue.conf.import_list1` import error."
    with pytest.raises(ImportError, match=msg):
        import_list(["meringue.conf.import_list1"])


def test_import_dict():
    """
    Verifying a successful dict import.
    """
    value = {"key": "meringue.conf.import_dict"}
    imported_dict = import_dict(value)
    assert imported_dict == {"key": import_dict}


def test_import_dict_wrong_type():
    """
    Checking for a data type error when importing a dict.
    """
    msg = "`bool` data type is not supported for import."
    with pytest.raises(TypeError, match=msg):
        import_dict({"key": True})


def test_import_dict_non_existent():
    """
    Import error check for a dict.
    """
    msg = "`meringue.conf.import_dict1` import error."
    with pytest.raises(ImportError, match=msg):
        import_dict({"key": "meringue.conf.import_dict1"})


def test_import_parameter():
    """
    Checking for a successful import for a string.
    """
    imported_method = import_parameter("meringue.conf.import_parameter")
    assert imported_method == import_parameter


def test_import_parameter_non_existent():
    """
    Import error check for a string.
    """
    msg = "`meringue.conf.import_parameter1` import error."
    with pytest.raises(ImportError, match=msg):
        import_parameter("meringue.conf.import_parameter1")


@patch("meringue.conf.import_list", return_value="test")
def test_import_parameter_list(mocked_import):
    """
    Checking for a successful import for a list.
    """
    imported_list = import_parameter(["meringue.conf.import_parameter"])
    assert imported_list == "test"
    mocked_import.assert_called_once_with(["meringue.conf.import_parameter"])


@patch("meringue.conf.import_dict", return_value="test")
def test_import_parameter_dict(mocked_import):
    """
    Checking for a successful import for a dict.
    """
    imported_dict = import_parameter({"key": "meringue.conf.import_parameter"})
    assert imported_dict == "test"
    mocked_import.assert_called_once_with({"key": "meringue.conf.import_parameter"})


def test_import_parameter_unsupported_type():
    """
    Checking for an unsupported data type for import
    """
    msg = "`float` data type is not supported for import."
    with pytest.raises(TypeError, match=msg):
        import_parameter(1.0)
