# -*- coding: utf-8 -*-

import logging  # noqa

import django.db.models.options as options


logger = logging.getLogger('meringue')


options.DEFAULT_NAMES = options.DEFAULT_NAMES + (
    'translate_fields',
    # 'host_name',
    # 'view',
    # 'reverse_args',
)
