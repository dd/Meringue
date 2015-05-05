# -*- coding: utf-8 -*-


import logging
import re
import sys
import os

from django.conf import settings
from django.template import Library
from django.utils import timezone
from django.utils.module_loading import import_string

from meringue import settings as m_settings, errors


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


def _load_file(path):
    for sfinder in settings.STATICFILES_FINDERS:
        finder = import_string(sfinder)
        match = finder().find(path)
        if match:
            break

    if not match:
        raise errors.FileNotFindError(os.path.split(path)[1])
    return open(match, 'r')


def _get_min_path(path):
    return re.sub(
        re.compile(ur'^(?P<name>[\w\W]*).(?P<type>css|js)$', re.UNICODE),
        lambda m: '%s.min.%s' % (m.groupdict()['name'],
                                 m.groupdict()['type']),
        path
    )


def _load_static_file(path, try_load_min=True):
    file = None
    if try_load_min:
        try:
            file = _load_file( _get_min_path(path) )
        except errors.FileNotFindError:
            pass

    if not file:
        file = _load_file(path)

    return file


@register.simple_tag
def put_css(path):
    '''
        Тег выводит содержимое css файла инлайном при этом приобразуя
        относительные пути, при этом пытается вывести минифицированный
        вариант файла
    '''
    result_wrapper = "<style>%s</style>"

    try:
        file = _load_static_file(path, not settings.DEBUG)
    except errors.FileNotFindError, error:
        if settings.TEMPLATE_DEBUG:
            return u'<script type=\"text/javascript\">console.log(\"файл\
 %s ненайден\"); </script>' % path
        raise error

    return result_wrapper % re.sub(
        re.compile(ur'url\(("|\'|\ |)(\.\.\/)(?P<path>[^\"\'\)]+)("|\'|)\)',
                   re.MULTILINE | re.UNICODE),
        lambda m: 'url(%s%s)' % (settings.STATIC_URL, m.groupdict()['path']),
        file.read()
    )


@register.simple_tag
def put_js(path):
    '''
        Тег выводит содержимое js файла инлайном при этом приобразуя
        относительные пути, при этом пытается вывести минифицированный
        вариант файла
    '''
    result_wrapper = "<script type=\"text/javascript\">%s</script>"

    try:
        file = _load_static_file(path, not settings.DEBUG)
    except errors.FileNotFindError, error:
        if settings.TEMPLATE_DEBUG:
            return u'<script type=\"text/javascript\">console.log(\"файл\
 %s ненайден\"); </script>' % path
        raise error

    return result_wrapper % file.read()


@register.simple_tag
def put_reset():
    '''
    Шаблонный тег выводит содержимое файла reset.css заключённое в тег style
    '''
    return '<style>%s</style>' % open(m_settings.path('meringue/static/css/reset%s.css' % '' if settings.DEBUG else '.min'), 'r').read()
