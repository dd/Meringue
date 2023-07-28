from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class Config(AppConfig):
    name = "meringue.api"
    verbose_name = _("API")
    label = "meringue_api"
