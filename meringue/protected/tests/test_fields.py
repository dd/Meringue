import pytest
from faker import Faker
from io import BytesIO
from unittest.mock import patch

import django
from django.contrib.contenttypes.models import ContentType
from django.core.files.uploadedfile import UploadedFile
from django.test import Client
from django.test import override_settings
from django.urls import reverse

from test_project.models import ProtectedModel

IS_DJANGO_2 = django.VERSION < (3,)
IS_DJANGO_3 = django.VERSION < (4,)
if IS_DJANGO_2 or IS_DJANGO_3:
    from django.core.files.storage import FileSystemStorage
else:
    from django.core.files.storage.filesystem import FileSystemStorage


faker = Faker()


@pytest.mark.django_db
def test_protectedfields(file_uploaded, image_uploaded):
    instance = ProtectedModel.objects.create(file=file_uploaded, image=image_uploaded)

    assert instance.file.url == "/protected/6/file/1"
    assert instance.image.url == "/protected/6/image/1"


@pytest.mark.django_db
def test_protected_file_view_403():
    url = reverse(
        "meringue-protected-file",
        kwargs={
            "contenttype_id": ContentType.objects.get_for_model(ProtectedModel).id,
            "field": "file",
            "pk": 1,
        },
    )
    response = Client().get(url)

    assert response.status_code == 403


@patch(
    "django.contrib.auth.models.AnonymousUser.has_perm",
    return_value=lambda *a, **k: True,
)
@pytest.mark.django_db
def test_protected_file_view_404(mocked_has_perm):
    instance = ProtectedModel.objects.create()

    url = reverse(
        "meringue-protected-file",
        kwargs={
            "contenttype_id": ContentType.objects.get_for_model(ProtectedModel).id,
            "field": "file",
            "pk": instance.id,
        },
    )
    response = Client().get(url)

    assert response.status_code == 404


@patch(
    "django.contrib.auth.models.AnonymousUser.has_perm",
    return_value=True,
)
@override_settings(MERINGUE={"PROTECTED_SERVE_WITH_NGINX": False})
@pytest.mark.django_db
def test_protected_file_view_file_response(mocked_has_perm):
    FileSystemStorage().delete("protected/test.bin")

    file_uploaded = UploadedFile(BytesIO(faker.binary()), name="test.bin")
    instance = ProtectedModel.objects.create(file=file_uploaded)

    response = Client().get(instance.file.url)

    assert response.status_code == 200
    assert response.get('Content-Length') == str(instance.file.size)
    if not IS_DJANGO_2:
        assert response.get('Content-Disposition') == f'inline; filename="test.bin"'


@patch(
    "django.contrib.auth.models.AnonymousUser.has_perm",
    return_value=True,
)
@override_settings(MERINGUE={"PROTECTED_SERVE_WITH_NGINX": True})
@pytest.mark.django_db
def test_protected_file_view_nginx(mocked_has_perm):
    FileSystemStorage().delete("protected/тест.png")

    image_uploaded = UploadedFile(BytesIO(faker.image(image_format="png")), name="тест.png")
    instance = ProtectedModel.objects.create(image=image_uploaded)

    response = Client().get(instance.image.url)

    assert response.status_code == 200
    assert response.get("Content-Type") == "image/png"
    assert response.get("Content-Disposition") == "inline; filename=%D1%82%D0%B5%D1%81%D1%82.png"
    if IS_DJANGO_2:
        assert response.get("X-Accel-Redirect") == "media/protected/%D1%82%D0%B5%D1%81%D1%82.png"
    else:
        assert response.get("X-Accel-Redirect") == "/media/protected/%D1%82%D0%B5%D1%81%D1%82.png"


@patch(
    "django.contrib.auth.models.AnonymousUser.has_perm",
    return_value=True,
)
@override_settings(MERINGUE={"PROTECTED_SERVE_WITH_NGINX": True})
@pytest.mark.django_db
def test_protected_file_view_nginx_origfiles(mocked_has_perm):
    FileSystemStorage().delete("тест_orig.png")

    image_uploaded = UploadedFile(BytesIO(faker.image(image_format="png")), name="тест_orig.png")
    instance = ProtectedModel.objects.create(image_orig=image_uploaded)

    url = reverse(
        "meringue-protected-file",
        kwargs={
            "contenttype_id": ContentType.objects.get_for_model(ProtectedModel).id,
            "field": "image_orig",
            "pk": instance.id,
        },
    )
    response = Client().get(url)

    assert response.status_code == 200
    assert response.get("Content-Type") == "image/png"
    assert response.get("Content-Disposition") == (
        "inline; filename=%D1%82%D0%B5%D1%81%D1%82_orig.png"
    )
    if IS_DJANGO_2:
        assert response.get("X-Accel-Redirect") == "media/%D1%82%D0%B5%D1%81%D1%82_orig.png"
    else:
        assert response.get("X-Accel-Redirect") == "/media/%D1%82%D0%B5%D1%81%D1%82_orig.png"
