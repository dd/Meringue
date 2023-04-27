# -*- coding:utf-8 -*-

import os
import uuid

from django.conf import settings
from django.utils import timezone


__all__ = ['THUMBNAIL_DEBUG', 'THUMBNAIL_PROPERTIES', 'THUMBNAIL_METHODS', 'THUMBNAIL_CROP_METHOD',
           'THUMBNAIL_RESIZE_METHOD', 'THUMBNAIL_QUALITY', 'THUMBNAIL_COLOR', 'THUMBNAIL_BG_COLOR',
           'THUMBNAIL_DIR', 'THUMBNAIL_URL', 'START_YEAR',]


########
# CORE #
########


# upload handlers #

def UPLOAD_RENAME_HANDLER(result):
    return u'{0}{1}'.format(uuid.uuid4(), os.path.splitext(result.name)[1])


# thumbnail #

THUMBNAIL_DEBUG = False
THUMBNAIL_PROPERTIES = {}
THUMBNAIL_METHODS = {}
THUMBNAIL_CROP_METHOD = ['center', 'center']
THUMBNAIL_RESIZE_METHOD = 'cover'
THUMBNAIL_QUALITY = 100
THUMBNAIL_COLOR = (255, 255, 255, 0)
THUMBNAIL_BG_COLOR = (200, 200, 200, 0)
THUMBNAIL_DIR = os.path.join(settings.MEDIA_ROOT, 'temp')
THUMBNAIL_URL = settings.MEDIA_URL + 'temp/'


# copyright year #

START_YEAR = timezone.now().year
