import pytest
from io import BytesIO

from django.core.files.uploadedfile import UploadedFile

from faker import Faker


faker = Faker()


@pytest.fixture
def file_uploaded():
    return UploadedFile(BytesIO(faker.binary()), name=faker.file_name())

@pytest.fixture
def image_uploaded():
    return UploadedFile(BytesIO(faker.image()), name=faker.file_name())
