from django.db.models import options


options.DEFAULT_NAMES = (
    *options.DEFAULT_NAMES,
    'translate_fields',
    # 'host_name',
    # 'view',
    # 'reverse_args',
)
