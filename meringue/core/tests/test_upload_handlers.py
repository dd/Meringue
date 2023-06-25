from io import BytesIO
from unittest.mock import patch

from django.test import Client
from django.test import override_settings
from django.urls import reverse

from meringue.core.upload_handlers import MemoryFileUploadHandler
from meringue.core.upload_handlers import TemporaryFileUploadHandler


@override_settings(
    MERINGUE={"UPLOAD_RENAME_HANDLER": "test_project.upload_handlers.rename_handler"},
    FILE_UPLOAD_HANDLERS=(
        "meringue.core.upload_handlers.TemporaryFileUploadHandler",
        "meringue.core.upload_handlers.MemoryFileUploadHandler",
    ),
)
@patch(
    "meringue.core.upload_handlers.MemoryFileUploadHandler.new_file",
    autospec=True,
    side_effect=MemoryFileUploadHandler.new_file,
)
def test_upload_file_to_memory(mocked_new_file):
    """
    Check upload file with MemoryFileUploadHandler
    """

    img = BytesIO()
    img.name = "foo.gif"

    response = Client().post(reverse("upload_file"), {"file": img})

    assert response.status_code == 200
    mocked_new_file.assert_called_once()
    assert response.json()["file"] == "new_file_name.gif"


@override_settings(
    MERINGUE={"UPLOAD_RENAME_HANDLER": "test_project.upload_handlers.rename_handler"},
    FILE_UPLOAD_HANDLERS=("meringue.core.upload_handlers.TemporaryFileUploadHandler",),
)
@patch(
    "meringue.core.upload_handlers.TemporaryFileUploadHandler.new_file",
    autospec=True,
    side_effect=TemporaryFileUploadHandler.new_file,
)
def test_upload_file_temp(mocked_new_file):
    """
    Check upload file with TemporaryFileUploadHandler
    """

    img = BytesIO()
    img.name = "foo.gif"

    response = Client().post(reverse("upload_file"), {"file": img})

    assert response.status_code == 200
    mocked_new_file.assert_called_once()
    assert response.json()["file"] == "new_file_name.gif"
