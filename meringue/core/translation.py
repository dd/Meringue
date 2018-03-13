# -*- coding: utf-8 -*-

import logging  # noqa

from importlib import import_module

from django.conf import settings

from modeltranslation.translator import translator, TranslationOptions


logger = logging.getLogger('meringue')


for app in settings.INSTALLED_APPS:
    try:
        models = import_module('%s.models' % app)
    except ImportError:
        bits = app.split('.')
        app = import_module(bits[0])

        for bit in bits[1:]:
            app = getattr(app, bit)

        if hasattr(app, 'name'):
            try:
                models = import_module('%s.models' % app.name)
            except ImportError:
                continue
        else:
            continue
    except AttributeError:
        continue

    for mod in getattr(models, 'translate_models', []):
        unit = getattr(models, mod)
        translator.register(
            unit,
            type(
                str(mod + 'Translation'),
                (TranslationOptions,),
                {'fields': getattr(unit._meta, 'translate_fields', list())}
            )
        )
