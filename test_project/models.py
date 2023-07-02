from django.db import models

from meringue.core.models import CMTimeMixin
from meringue.core.models import PublicationDatesMixin
from meringue.core.models import PublicationMixin
from meringue.core.models import SortingMixin


class CMTimeModel(CMTimeMixin):
    title = models.CharField(max_length=32)


class SortingModel(SortingMixin):
    title = models.CharField(max_length=32)


class PublicationModel(PublicationMixin):
    title = models.CharField(max_length=32)


class PublicationDatesModel(PublicationDatesMixin):
    title = models.CharField(max_length=32)


class TranslatedModel(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        m_translate_fields = [
            "name",
        ]
