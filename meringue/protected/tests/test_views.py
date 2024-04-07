from io import BytesIO
from unittest.mock import PropertyMock
from unittest.mock import patch

import django
from django.contrib.contenttypes.models import ContentType
from django.core.files.uploadedfile import UploadedFile
from django.test import Client
from django.test import override_settings
from django.urls import reverse

import pytest
from faker import Faker

from test_project.models import ProtectedModel


IS_DJANGO_2 = (2,) <= django.VERSION < (3,)
IS_DJANGO_20 = (2, 0) <= django.VERSION < (2, 1)
IS_DJANGO_3 = (3,) <= django.VERSION < (4,)
IS_DJANGO_GTE_3 = django.VERSION >= (3,)
if IS_DJANGO_2 or IS_DJANGO_3:
    from django.core.files.storage import FileSystemStorage
else:
    from django.core.files.storage.filesystem import FileSystemStorage


faker = Faker()


@pytest.mark.django_db
def test_x_accel_redirect_view_403():
    url = reverse(
        "x_accel_redirect_view",
        kwargs={
            "cid": ContentType.objects.get_for_model(ProtectedModel).id,
            "field": "file",
            "pk": 1,
            "disp": "inline",
        },
    )
    response = Client().get(url)

    assert response.status_code == 403


@pytest.mark.django_db
def test_x_accel_redirect_view_404(mocked_has_perm_true):
    instance = ProtectedModel.objects.create()

    url = reverse(
        "x_accel_redirect_view",
        kwargs={
            "cid": ContentType.objects.get_for_model(ProtectedModel).id,
            "field": "file",
            "pk": instance.id,
            "disp": "inline",
        },
    )
    response = Client().get(url)

    assert response.status_code == 404


@override_settings(MERINGUE={"PROTECTED_SERVE_WITH_NGINX": False})
@pytest.mark.django_db
def test_x_accel_redirect_view_file_response(mocked_has_perm_true):
    FileSystemStorage().delete("protected/test_file_response.bin")
    FileSystemStorage().delete("protected/test_file_response.png")

    file_uploaded = UploadedFile(BytesIO(faker.binary()), name="test_file_response.bin")
    image_uploaded = UploadedFile(BytesIO(faker.binary()), name="test_file_response.png")
    instance = ProtectedModel.objects.create(file=file_uploaded, image=image_uploaded)

    file_response = Client().get(instance.file.url)
    assert file_response.status_code == 200
    assert file_response.get("Content-Length") == str(instance.file.size)

    image_response = Client().get(instance.image.url)
    assert image_response.status_code == 200
    assert image_response.get("Content-Length") == str(instance.image.size)


@override_settings(MERINGUE={"PROTECTED_SERVE_WITH_NGINX": False})
@pytest.mark.django_db
def test_x_accel_redirect_view_file_response_disposition(mocked_has_perm_true):
    FileSystemStorage().delete("protected/test_disposition.bin")
    FileSystemStorage().delete("protected/test_disposition.png")

    file_uploaded = UploadedFile(BytesIO(faker.binary()), name="test_disposition.bin")
    image_uploaded = UploadedFile(BytesIO(faker.binary()), name="test_disposition.png")
    instance = ProtectedModel.objects.create(file=file_uploaded, image=image_uploaded)

    file_response = Client().get(instance.file.url)
    image_response = Client().get(instance.image.url)

    if IS_DJANGO_20:
        assert "Content-Disposition" not in file_response
        assert "Content-Disposition" not in image_response

    elif IS_DJANGO_2:
        assert file_response.get("Content-Disposition") == (
            'attachment; filename="test_disposition.bin"'
        )
        assert "Content-Disposition" not in image_response

    elif IS_DJANGO_GTE_3:
        assert file_response.get("Content-Disposition") == (
            'attachment; filename="test_disposition.bin"'
        )
        assert image_response.get("Content-Disposition") == (
            'inline; filename="test_disposition.png"'
        )


@override_settings(MERINGUE={"PROTECTED_SERVE_WITH_NGINX": True})
@pytest.mark.django_db
def test_x_accel_redirect_view_nginx(mocked_has_perm_true):
    FileSystemStorage().delete("protected/тест_with_nginx.png")

    image_uploaded = UploadedFile(
        BytesIO(faker.image(image_format="png")), name="тест_with_nginx.png"
    )
    instance = ProtectedModel.objects.create(image=image_uploaded)

    response = Client().get(instance.image.url)

    assert response.status_code == 200
    assert response.get("Content-Type") == "image/png"
    assert response.get("Content-Disposition") == (
        "inline; filename=%D1%82%D0%B5%D1%81%D1%82_with_nginx.png"
    )

    image_url = "media/protected/%D1%82%D0%B5%D1%81%D1%82_with_nginx.png"
    if not IS_DJANGO_2:
        image_url = f"/{image_url}"

    assert response.get("X-Accel-Redirect") == image_url


@patch(
    "meringue.protected.fields.ProtectedFileMixin.redirect_url",
    new_callable=PropertyMock,
    return_value="/test_file_url",
)
@override_settings(MERINGUE={"PROTECTED_SERVE_WITH_NGINX": True})
@pytest.mark.django_db
def test_x_accel_redirect_redirect_url_usage(
    mocked_redirect_url,
    mocked_has_perm_true,
    file_uploaded,
    image_uploaded,
):
    instance = ProtectedModel.objects.create(file=file_uploaded, image=image_uploaded)

    response = Client().get(instance.file.url)
    assert response["X-Accel-Redirect"] == "/test_file_url"
    mocked_redirect_url.assert_called_once_with()

    response = Client().get(instance.image.url)
    assert response["X-Accel-Redirect"] == "/test_file_url"
    assert mocked_redirect_url.call_count == 2
    mocked_redirect_url.assert_called()


@override_settings(MERINGUE={"PROTECTED_SERVE_WITH_NGINX": True})
@pytest.mark.django_db
def test_x_accel_redirect_view_nginx_origfiles(mocked_has_perm_true):
    FileSystemStorage().delete("тест_orig.png")

    image_uploaded = UploadedFile(BytesIO(faker.image(image_format="png")), name="тест_orig.png")
    instance = ProtectedModel.objects.create(image_orig=image_uploaded)

    url = reverse(
        "x_accel_redirect_view",
        kwargs={
            "cid": ContentType.objects.get_for_model(ProtectedModel).id,
            "field": "image_orig",
            "pk": instance.id,
            "disp": "inline",
        },
    )
    response = Client().get(url)

    assert response.status_code == 200
    assert response.get("Content-Type") == "image/png"
    assert response.get("Content-Disposition") == (
        "inline; filename=%D1%82%D0%B5%D1%81%D1%82_orig.png"
    )

    image_url = "media/%D1%82%D0%B5%D1%81%D1%82_orig.png"
    if not IS_DJANGO_2:
        image_url = f"/{image_url}"

    assert response.get("X-Accel-Redirect") == image_url
