from meringue.conf import m_settings


def test_m_settings():
    """
    Checking that the module with meringue settings works
    """
    assert m_settings.UPLOAD_RENAME_HANDLER
