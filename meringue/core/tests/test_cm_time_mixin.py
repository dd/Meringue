import pytest
from faker import Faker

from test_project.models import CMTimeModel


fake = Faker()


@pytest.mark.django_db
def test_cmtimemixin():
    """
    Nominal mixin check
    """
    instance = CMTimeModel.objects.create(title=fake.name())
    assert instance.ctime
    assert instance.mtime
