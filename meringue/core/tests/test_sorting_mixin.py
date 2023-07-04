import pytest
from faker import Faker

from test_project.models import SortingModel


fake = Faker()


@pytest.mark.django_db
def test_correction_sorting():
    """
    Checking the sort fix
    """

    instance1 = SortingModel.objects.create(title=fake.name(), sorting=0)
    instance2 = SortingModel.objects.create(title=fake.name(), sorting=0)
    instance3 = SortingModel.objects.create(title=fake.name(), sorting=0)

    SortingModel.objects.order_by("sorting", "id").correction_sorting()

    instance1.refresh_from_db()
    instance2.refresh_from_db()
    instance3.refresh_from_db()

    assert instance1.sorting == 0
    assert instance2.sorting == 1
    assert instance3.sorting == 2


@pytest.mark.django_db
def test_correction_sorting_with_filtration():
    """
    Checking the sort fix for filtered queryset
    """

    instance1 = SortingModel.objects.create(title=fake.name(), sorting=0)
    instance2 = SortingModel.objects.create(title=fake.name(), sorting=0)
    instance3 = SortingModel.objects.create(title=fake.name(), sorting=0)

    SortingModel.objects.filter(id__in=["1", "2"]).order_by("sorting", "id").correction_sorting()

    instance1.refresh_from_db()
    instance2.refresh_from_db()
    instance3.refresh_from_db()

    assert instance1.sorting == 0
    assert instance2.sorting == 1
    assert instance3.sorting == 0
