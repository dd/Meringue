import django

from meringue.core import options

if django.VERSION < (3, 2):
    default_app_config = "meringue.core.apps.Config"
