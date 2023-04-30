from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class Config(AppConfig):
    name = 'meringue.core'
    verbose_name = _('Зефирка')  # noqa: RUF001
    label = 'meringue'
