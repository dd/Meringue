from django.db.models import options


options.DEFAULT_NAMES = (
    *options.DEFAULT_NAMES,
    "translate_fields",
)
