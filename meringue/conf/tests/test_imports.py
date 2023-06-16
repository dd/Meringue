# ruff: noqa: S101

import pytest

from meringue.conf import import_from_string


def test__import():
    """
    Checking if modules were imported successfully
    """
    imported_method = import_from_string("meringue.conf.import_from_string", None)
    assert imported_method == import_from_string


def test__import_error():
    """
    Checking if modules were imported successfully
    """
    msg = (
        "Could not import 'meringue.conf.not_exists_method' for API setting 'TEST'."
        '\nImportError: Module "meringue.conf" does not define a "not_exists_method" '
        "attribute/class."
    )
    with pytest.raises(ImportError, match=msg):
        import_from_string("meringue.conf.not_exists_method", "TEST")
