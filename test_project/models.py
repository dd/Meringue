from django.db import models

from meringue.core.models import CMTimeMixin
from meringue.core.models import PublicationDatesMixin
from meringue.core.models import PublicationMixin
from meringue.core.models import SortingMixin
from meringue.protected.fields import ProtectedFileField
from meringue.protected.fields import ProtectedImageField


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
        m_translate_fields = ["name"]


def _test_getter(field_file):
    return "/test_url"


class ProtectedModel(models.Model):
    file = ProtectedFileField(view_name="x_accel_redirect_view")
    image = ProtectedImageField(view_name="x_accel_redirect_view", disposition="inline")
    file_hosts = ProtectedFileField(
        view_name="sub-x_accel_redirect_view", host_name="sub", disposition="inline"
    )
    image_hosts = ProtectedImageField(view_name="sub-x_accel_redirect_view", host_name="sub")
    file_getter = ProtectedFileField(view_name="x_accel_redirect_view", nginx_location_getter=_test_getter)
    image_getter = ProtectedImageField(view_name="x_accel_redirect_view", nginx_location_getter=_test_getter)
    file_orig = models.FileField()
    image_orig = models.ImageField()
