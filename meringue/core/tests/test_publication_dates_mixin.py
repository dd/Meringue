import datetime as dt
from unittest.mock import patch

import pytest
import pytz
from faker import Faker

from test_project.models import PublicationDatesModel


fake = Faker()


@pytest.fixture(scope="module")
def items(django_db_blocker):
    with django_db_blocker.unblock():
        PublicationDatesModel.objects.create(title=fake.name(), date_from=None, date_to=None)
        PublicationDatesModel.objects.create(
            title=fake.name(),
            date_from=dt.datetime(2023, 1, 1, 0, 0, 0, tzinfo=pytz.utc),
            date_to=None,
        )
        PublicationDatesModel.objects.create(
            title=fake.name(),
            date_from=None,
            date_to=dt.datetime(2023, 1, 2, 0, 0, 0, tzinfo=pytz.utc),
        )
        PublicationDatesModel.objects.create(
            title=fake.name(),
            date_from=dt.datetime(2023, 1, 2, 0, 0, 0, tzinfo=pytz.utc),
            date_to=None,
        )
        PublicationDatesModel.objects.create(
            title=fake.name(),
            date_from=None,
            date_to=dt.datetime(2023, 1, 1, 0, 0, 0, tzinfo=pytz.utc),
        )


@pytest.mark.django_db
@patch("django.utils.timezone.now")
def test_published(mocked_now, items):
    """
    Check filtering published items
    """

    mocked = dt.datetime(2023, 1, 1, 0, 0, 0, tzinfo=pytz.utc)
    mocked_now.return_value = mocked

    assert PublicationDatesModel.objects.published().count() == 3


@pytest.mark.django_db
@patch("django.utils.timezone.now")
def test_unpublished(mocked_now, items):
    """
    Check filtering unpublished items
    """

    mocked = dt.datetime(2023, 1, 1, 0, 0, 0, tzinfo=pytz.utc)
    mocked_now.return_value = mocked

    assert PublicationDatesModel.objects.unpublished().count() == 2
