# -*- coding:utf-8 -*-

import os
import uuid

from django.conf import settings
from django.utils import timezone

########
# HOST #
########

PORT = getattr(
    settings,
    'MERINGUE_SITE_PORT',
    None
)


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

THUMBNAIL_DEBUG = getattr(
    settings,
    'MERINGUE_THUMBNAIL_DEBUG',
    False
)
THUMBNAIL_PROPERTIES = getattr(
    settings,
    'MERINGUE_THUMBNAIL_PROPERTIES',
    {}
)
THUMBNAIL_METHODS = getattr(
    settings,
    'MERINGUE_THUMBNAIL_METHODS',
    {}
)
THUMBNAIL_CROP_METHOD = getattr(
    settings,
    'MERINGUE_THUMBNAIL_CROP_METHOD',
    ['center', 'center']
)
THUMBNAIL_RESIZE_METHOD = getattr(
    settings,
    'MERINGUE_THUMBNAIL_RESIZE_METHOD',
    'cover'
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


###################
# UPLOAD HANDLERS #
###################

def _rename(result):
    return u'{0}{1}'.format(uuid.uuid4(), os.path.splitext(result.name)[1])

UPLOAD_HANDLER_RENAME_FN = getattr(
    settings,
    'MERINGUE_UPLOAD_HANDLER_RENAME_FN',
    _rename
)


############
# UNIFYING #
############

DEFAULT_PHONE_LOCALIZATION = getattr(
    settings,
    'MERINGUE_DEFAULT_PHONE_LOCALIZATION',
    'RU'
)


##############
# PUT CSS/JS #
##############

LOAD_MINI = getattr(
    settings,
    'MERINGUE_LOAD_MINI',
    not settings.DEBUG
)
