import pytest

from django.contrib.contenttypes.models import ContentType
from django.test import override_settings

from test_project.models import ProtectedModel


@pytest.mark.django_db
def test_protectedfields(file_uploaded, image_uploaded):
    instance = ProtectedModel.objects.create(file=file_uploaded, image=image_uploaded)
    cid = ContentType.objects.get_for_model(ProtectedModel).id

    assert instance.file.url == f"/protected/{cid}/file/{instance.id}"
    assert instance.image.url == f"/protected/{cid}/image/{instance.id}"


@override_settings(
    DEFAULT_HOST="default",
    PARENT_HOST="example.com",
    ROOT_HOSTCONF="test_project.hosts",
)
@pytest.mark.django_db
def test_protectedfields_hosts(file_uploaded):
    cid = ContentType.objects.get_for_model(ProtectedModel).id
    instance = ProtectedModel.objects.create(file_hosts=file_uploaded)

    assert instance.file_hosts.url == f"//sub.example.com/protected/{cid}/file_hosts/{instance.id}"
