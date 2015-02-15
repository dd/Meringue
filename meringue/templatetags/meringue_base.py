# -*- coding: utf-8 -*-


import logging
import re

from django.conf import settings
from django.template import Library
from django.utils import timezone
from django.utils.module_loading import import_string

from meringue import settings as m_settings


register = Library()

@register.simple_tag
def cop_year():
    '''
    Шаблонный тег возвращает диапозон годов для футера в формате:
        YYYY-YYYY
        YYYY

    Год старта проекта указывается в settings проекта - START_YEAR
    '''

    year = timezone.now().year
    return year == m_settings.START_YEAR and year or '%d&mdash;%d' %\
        (m_settings.START_YEAR, year)


@register.simple_tag
def put_static(path):
    '''
    Тег выводит содержимое файла инлайном при этом приобразуя относительные пути
    '''
    for sfinder in settings.STATICFILES_FINDERS:
        finder = import_string(sfinder)
        match = finder().find(path)
        if match:
            break
    if not match and settings.TEMPLATE_DEBUG:
        return '<script type=\"text/javascript\"> console.log(\"файл %s не\
найден\"); </script>' % path
    elif not match:
        return ''

    return re.sub(
        re.compile(ur'url\(("|\'|\ |)(\.\.\/)(?P<path>[^\"\'\)]+)("|\'|)\)',
                   re.MULTILINE | re.UNICODE),
        lambda m: 'url(%s%s)' % (settings.STATIC_URL, m.groupdict()['path']),
        open(match, 'r').read()
    )


@register.simple_tag
def put_reset():
    '''
    Шаблонный тег выводит содержимое файла reset.css заключённое в тег style
    '''
    return '<style>%s</style>' % open(m_settings.path('meringue/static/css/reset%s.css' % '' if settings.DEBUG else '.min'), 'r').read()
