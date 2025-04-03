from io import BytesIO

import django
from django.contrib.contenttypes.models import ContentType
from django.core.files.uploadedfile import UploadedFile
from django.test import override_settings

import pytest
from faker import Faker

from test_project.models import ProtectedModel


IS_DJANGO_2 = (2,) <= django.VERSION < (3,)
IS_DJANGO_3 = (3,) <= django.VERSION < (4,)
if IS_DJANGO_2 or IS_DJANGO_3:
    from django.core.files.storage import FileSystemStorage
else:
    from django.core.files.storage.filesystem import FileSystemStorage


faker = Faker()


@pytest.mark.django_db
def test_protectedfields_url(file_uploaded, image_uploaded):
    instance = ProtectedModel.objects.create(file=file_uploaded, image=image_uploaded)
    cid = ContentType.objects.get_for_model(ProtectedModel).id

    assert instance.file.url == f"/protected/{cid}/file/{instance.id}/attachment"
    assert instance.image.url == f"/protected/{cid}/image/{instance.id}/inline"


@override_settings(
    DEFAULT_HOST="default",
    PARENT_HOST="example.com",
    ROOT_HOSTCONF="test_project.hosts",
)
@pytest.mark.django_db
def test_protectedfields_hosts(file_uploaded, image_uploaded):
    cid = ContentType.objects.get_for_model(ProtectedModel).id
    instance = ProtectedModel.objects.create(file_hosts=file_uploaded, image_hosts=image_uploaded)

    file_hosts_url = f"//sub.example.com/protected/{cid}/file_hosts/{instance.id}/inline"
    assert instance.file_hosts.url == file_hosts_url

    image_hosts_url = f"//sub.example.com/protected/{cid}/image_hosts/{instance.id}/attachment"
    assert instance.image_hosts.url == image_hosts_url


@pytest.mark.django_db
def test_protectedfields_original_url():
    FileSystemStorage().delete("protected/test_original_url.bin")
    FileSystemStorage().delete("protected/test_original_url.png")
    file_uploaded = UploadedFile(BytesIO(faker.binary()), name="test_original_url.bin")
    image_uploaded = UploadedFile(BytesIO(faker.image()), name="test_original_url.png")
    instance = ProtectedModel.objects.create(file=file_uploaded, image=image_uploaded)

    file_url = "media/protected/test_original_url.bin"
    image_url = "media/protected/test_original_url.png"

    if not IS_DJANGO_2:
        file_url = f"/{file_url}"
        image_url = f"/{image_url}"

    assert instance.file.original_url == file_url
    assert instance.image.original_url == image_url


@pytest.mark.django_db
def test_protectedfields_redirect_url(file_uploaded, image_uploaded):
    FileSystemStorage().delete("protected/test_redirect_url.bin")
    FileSystemStorage().delete("protected/test_redirect_url.png")
    file_uploaded = UploadedFile(BytesIO(faker.binary()), name="test_redirect_url.bin")
    image_uploaded = UploadedFile(BytesIO(faker.image()), name="test_redirect_url.png")

    instance = ProtectedModel.objects.create(file=file_uploaded, image=image_uploaded)

    file_url = "media/protected/test_redirect_url.bin"
    image_url = "media/protected/test_redirect_url.png"

    if not IS_DJANGO_2:
        file_url = f"/{file_url}"
        image_url = f"/{image_url}"

    assert instance.file.redirect_url == file_url
    assert instance.image.redirect_url == image_url

    assert instance.file_getter.redirect_url == "/test_url"
    assert instance.image_getter.redirect_url == "/test_url"
