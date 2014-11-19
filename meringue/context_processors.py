# -*- coding: utf-8 -*-

from django.conf import settings


def base(request):
    return {
        'SITE_NAME': settings.SITE_NAME,
        'TEMPLATE_DEBUG': settings.TEMPLATE_DEBUG,
        'DEBUG': settings.DEBUG,
    }
