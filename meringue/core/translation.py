from django.apps import apps

from modeltranslation.translator import TranslationOptions
from modeltranslation.translator import translator


for model in apps.get_models():
    fields = getattr(model._meta, "m_translate_fields", [])

    if fields and model not in translator.get_registered_models():
        translator.register(
            model,
            type(
                str(model.__name__ + "Translation"),
                (TranslationOptions,),
                {"fields": fields},
            ),
        )
