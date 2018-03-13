# -*- coding: utf-8 -*-

import logging  # noqa

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class MeringueCoreConfig(AppConfig):
    name = 'meringue.core'
    verbose_name = _('Зефирка')
