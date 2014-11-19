# -*- coding:utf-8 -*-

import os

from django.conf import settings
from django.utils import timezone


##################
# current folder #
##################

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
path = lambda *args: os.path.join(BASE_DIR, *args).replace('\\', '/')


##################
# copyright year #
##################

START_YEAR = getattr(
    settings,
    'MERINGUE_START_YEAR',
    timezone.now().year
)


#############
# thumbnail #
#############

THUMBNAIL_CROP_MOTHOD = getattr(
    settings,
    'MERINGUE_THUMBNAIL_CROP_MOTHOD',
    ['center', 'center']
)
THUMBNAIL_RESIZE_MOTHOD = getattr(
    settings,
    'MERINGUE_THUMBNAIL_RESIZE_MOTHOD',
    'inscribe'
)
THUMBNAIL_QUALITY = getattr(
    settings,
    'MERINGUE_THUMBNAIL_QUALITY',
    100
)
THUMBNAIL_COLOR = getattr(
    settings,
    'MERINGUE_THUMBNAIL_COLOR',
    (255, 255, 255, 0)
)
THUMBNAIL_DIR = getattr(
    settings,
    'MERINGUE_THUMBNAIL_DIR',
    os.path.join(settings.MEDIA_ROOT, 'temp')
)
THUMBNAIL_URL = getattr(
    settings,
    'MERINGUE_THUMBNAIL_URL',
    settings.MEDIA_URL + 'temp/'
)


############
# UNIFYING #
############

DEFAULT_PHONE_LOCALIZATION = getattr(
    settings,
    'MERINGUE_DEFAULT_PHONE_LOCALIZATION',
    'RU'
)
