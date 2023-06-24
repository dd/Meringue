from django.db import models

from meringue.core.models import CMTimeMixin
from meringue.core.models import PublicationDatesMixin
from meringue.core.models import PublicationMixin
from meringue.core.models import SortingMixin


class CMTimeModel(CMTimeMixin):
    title = models.CharField(max_length=10)


class SortingModel(SortingMixin):
    title = models.CharField(max_length=10)


class PublicationModel(PublicationMixin):
    title = models.CharField(max_length=10)


class PublicationDatesModel(PublicationDatesMixin):
    title = models.CharField(max_length=10)
