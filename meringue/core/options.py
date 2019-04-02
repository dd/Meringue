# -*- coding: utf-8 -*-

import django.db.models.options as options


options.DEFAULT_NAMES = options.DEFAULT_NAMES + (
    'translate_fields',
    # 'host_name',
    # 'view',
    # 'reverse_args',
)
