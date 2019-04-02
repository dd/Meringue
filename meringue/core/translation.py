# -*- coding: utf-8 -*-

from importlib import import_module

from django.apps import apps
from django.conf import settings

from modeltranslation.translator import translator, TranslationOptions
try:
    from polymorphic.utils import get_base_polymorphic_model
except ImportError:
    get_base_polymorphic_model = None


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

    for model in apps.get_models():
        fields = getattr(model._meta, 'translate_fields', list())
        force = False

        if not fields and get_base_polymorphic_model and get_base_polymorphic_model(model):
            force = True

        if (fields or force) and not model in translator.get_registered_models():
            translator.register(
                model,
                type(
                    str(model.__name__ + 'Translation'),
                    (TranslationOptions, ),
                    {'fields': fields}
                )
            )
