# -*- coding: utf-8 -*-


import logging
import re
import sys
import os

from django.conf import settings
from django.template import Library
from django.utils import timezone
from django.utils.module_loading import import_string

from meringue import settings as m_settings
from meringue.errors import FileNotFindError


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


class PutStatic:

    def __init__(self, path, type, load_min=True, load=True, file=None,
                 fix_relative_path=True, fix_map_link=True):
        self.dir, self.filename = os.path.split(path)
        self.load_min = load_min
        self.type = type
        self.file = file
        self.fix_relative_path = fix_relative_path
        self.fix_map_link = fix_map_link

        if load and not file:
            self.file, self.minimal = self._load_static_file()
        else:
            self.file = file

    def _load_file(self, path):
        for backend_finder in settings.STATICFILES_FINDERS:
            finder = import_string(backend_finder)
            match = finder().find(path)
            if match:
                break

        if not match:
            raise FileNotFindError(os.path.split(path)[1])
        return open(match, 'r')

    def _get_min_filename(self):
        return re.sub(
            re.compile(ur'^(?P<name>[\w\W]*).(?P<type>css|js)$', re.UNICODE),
            lambda m: '%s.min.%s' % (m.groupdict()['name'],
                                     m.groupdict()['type']),
            self.filename
        )

    def _load_static_file(self):
        file = None

        if self.load_min:
            try:
                file = self._load_file(os.path.join(
                    self.dir,
                    self._get_min_filename()
                ))
                minimal = True
            except FileNotFindError:
                pass

        if not file:
            file = self._load_file(os.path.join(self.dir, self.filename))
            minimal = False

        return file, minimal

    def _fix_relative_path(self, text):
        if self.type == 'css':
            result = re.sub(
                re.compile(ur'url\(("|\'|\ |)(\.\.\/)(?P<path>[^\"\'\)]+)("|\'|)\)',
                           re.MULTILINE | re.UNICODE),
                lambda m: 'url(%s%s)' % (settings.STATIC_URL,
                                         m.groupdict()['path']),
                text
            )
        elif self.type == 'js':
            result = text
        return result

    def _fix_map_link(self, text):
        result = re.sub(
            re.compile(ur'sourceMappingURL=(?P<scheme>https:\/\/|http:\/\/|\/\/)?(?P<path>[\w\.]+)',
                       re.UNICODE),
            lambda m: 'sourceMappingURL=%s%s' % (settings.STATIC_URL,
                                                 m.groupdict()['path']),
            text
        )
        return result

    def read(self):
        if not self.file:
            self.file, self.minimal = self._load_static_file()

        result = self.file.read()

        if self.fix_relative_path:
            result = self._fix_relative_path(result)

        if self.fix_map_link:
            result = self._fix_map_link(result)

        return result


@register.simple_tag
def put_css(path):
    '''
        Тег выводит содержимое css файла инлайном при этом приобразуя
        относительные пути, при этом пытается вывести минифицированный
        вариант файла
    '''
    result_wrapper = "<style>%s</style>"

    try:
        file = PutStatic(path, 'css')  # , load_min=not settings.DEBUG)
    except FileNotFindError, error:
        if settings.TEMPLATE_DEBUG:
            return u'<script type=\"text/javascript\">console.log(\"файл\
 %s ненайден\"); </script>' % path
        raise error

    return result_wrapper % file.read()


@register.simple_tag
def put_js(path):
    '''
        Тег выводит содержимое js файла инлайном при этом приобразуя
        относительные пути, при этом пытается вывести минифицированный
        вариант файла
    '''
    result_wrapper = "<script type=\"text/javascript\">%s</script>"

    try:
        file = PutStatic(path, 'js')  # , load_min=not settings.DEBUG)
    except FileNotFindError, error:
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
