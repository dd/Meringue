# -*- coding:utf-8 -*-

import os

from django.conf import settings
from django.utils import timezone


START_YEAR = getattr(
    settings,
    'WO_SHEET_PAN_START_YEAR',
    timezone.now().year
)
THUMBNAIL_CROP_MOTHOD = getattr(
    settings,
    'WO_SHEET_PAN_THUMBNAIL_CROP_MOTHOD',
    ['center', 'center']
)
THUMBNAIL_RESIZE_MOTHOD = getattr(
    settings,
    'WO_SHEET_PAN_THUMBNAIL_RESIZE_MOTHOD',
    'inscribe'
)
THUMBNAIL_QUALITY = getattr(
    settings,
    'WO_SHEET_PAN_THUMBNAIL_QUALITY',
    100
)
THUMBNAIL_COLOR = getattr(
    settings,
    'WO_SHEET_PAN_THUMBNAIL_COLOR',
    (255, 255, 255, 0)
)
THUMBNAIL_DIR = getattr(
    settings,
    'WO_SHEET_PAN_THUMBNAIL_DIR',
    os.path.join(settings.MEDIA_ROOT, 'temp')
)
THUMBNAIL_URL = getattr(
    settings,
    'WO_SHEET_PAN_THUMBNAIL_URL',
    settings.MEDIA_URL + 'temp/'
)
