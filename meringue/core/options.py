from django.db.models import options


options.DEFAULT_NAMES = (
    *options.DEFAULT_NAMES,
    "m_translate_fields",
)
