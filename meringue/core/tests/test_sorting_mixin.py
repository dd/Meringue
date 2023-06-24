import pytest
from faker import Faker

from test_project.models import SortingModel


fake = Faker()


@pytest.mark.django_db
def test_cmtimemixin():
    """
    Check default value at sorting field
    """

    instance = SortingModel.objects.create(title=fake.name())
    assert instance.sorting == 0
