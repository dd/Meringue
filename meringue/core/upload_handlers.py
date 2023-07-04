import uuid
from pathlib import Path

from django.core.files import uploadhandler

from meringue.conf import m_settings


def rename_handler(file_name: str) -> str:
    """
    Default method for renaming files when using load handlers
    [MemoryFileUploadHandler][meringue.core.upload_handlers.MemoryFileUploadHandler] and / or
    [TemporaryFileUploadHandler][meringue.core.upload_handlers.TemporaryFileUploadHandler].

    Attributes:
        file_name: Original file name.

    Returns:
        New file name.
    """
    return str(Path(file_name).with_stem(str(uuid.uuid4())))


class MemoryFileUploadHandler(uploadhandler.MemoryFileUploadHandler):
    """
    File upload handler to stream uploads into memory (used for small files).

    Examples:
        ```py title="settings.py"
        FILE_UPLOAD_HANDLERS = (
            'meringue.core.upload_handlers.MemoryFileUploadHandler',
            'django.core.files.uploadhandler.TemporaryFileUploadHandler',
        )
        ```
    """

    def new_file(
        self,
        field_name,
        file_name,
        content_type,
        content_length,
        charset=None,
        content_type_extra=None,
    ):
        new_name = m_settings.UPLOAD_RENAME_HANDLER(file_name)
        super().new_file(
            field_name,
            new_name,
            content_type,
            content_length,
            charset,
            content_type_extra,
        )


class TemporaryFileUploadHandler(uploadhandler.TemporaryFileUploadHandler):
    """
    Upload handler that streams data into a temporary file.

    Examples:
        ```py title="settings.py"
        FILE_UPLOAD_HANDLERS = (
            'django.core.files.uploadhandler.MemoryFileUploadHandler',
            'meringue.core.upload_handlers.TemporaryFileUploadHandler',
        )
        ```
    """

    def new_file(
        self,
        field_name,
        file_name,
        content_type,
        content_length,
        charset=None,
        content_type_extra=None,
    ):
        new_name = m_settings.UPLOAD_RENAME_HANDLER(file_name)
        super().new_file(
            field_name,
            new_name,
            content_type,
            content_length,
            charset,
            content_type_extra,
        )
