import pytest
from faker import Faker

from test_project.models import PublicationModel


fake = Faker()


@pytest.mark.django_db
def test_published():
    """
    Check filtering published items
    """

    PublicationModel.objects.create(title=fake.name(), is_published=True)
    PublicationModel.objects.create(title=fake.name(), is_published=True)
    PublicationModel.objects.create(title=fake.name(), is_published=False)

    assert PublicationModel.objects.published().count() == 2


@pytest.mark.django_db
def test_unpublished():
    """
    Check filtering unpublished items
    """

    PublicationModel.objects.create(title=fake.name(), is_published=True)
    PublicationModel.objects.create(title=fake.name(), is_published=True)
    PublicationModel.objects.create(title=fake.name(), is_published=False)

    assert PublicationModel.objects.unpublished().count() == 1
