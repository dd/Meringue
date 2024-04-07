import pytest
from io import BytesIO
from unittest.mock import patch

from django.core.files.uploadedfile import UploadedFile

from faker import Faker


faker = Faker()


@pytest.fixture
def file_uploaded():
    return UploadedFile(BytesIO(faker.binary()), name=faker.file_name())

@pytest.fixture
def image_uploaded():
    return UploadedFile(BytesIO(faker.image()), name=faker.file_name())

@pytest.fixture
def mocked_has_perm_true(request):
    with patch(
        "django.contrib.auth.models.AnonymousUser.has_perm", return_value=True
    ) as mocked_has_perm:
        yield mocked_has_perm
