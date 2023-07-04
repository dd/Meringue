from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class Config(AppConfig):
    name = "meringue.core"
    verbose_name = _("Meringue")
    label = "meringue_core"
