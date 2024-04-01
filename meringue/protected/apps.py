from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class Config(AppConfig):
    name = "meringue.protected"
    verbose_name = _("Protected")
    label = "meringue_protected"
