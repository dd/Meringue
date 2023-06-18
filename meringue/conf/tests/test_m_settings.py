# ruff: noqa: S101

from meringue.conf import m_settings


def test__m_settings():
    """
    Checking that the module with meringue settings works
    """
    assert m_settings.UPLOAD_RENAME_HANDLER
