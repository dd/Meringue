from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class Config(AppConfig):
    name = 'meringue.admin'
    verbose_name = _('Админка')  # noqa: RUF001
    label = 'meringue_admin'
