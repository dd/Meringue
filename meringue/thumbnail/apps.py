from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class Config(AppConfig):
    name = "meringue.thumbnail"
    verbose_name = _("Превью")
    label = "meringue_thumbnail"
