# -*- coding: utf-8 -*-

from django.template import Library
from django.utils import timezone

from meringue import settings as wn_settings


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
    return year == wn_settings.START_YEAR and year or '%d&mdash;%d' %\
        (wn_settings.START_YEAR, year)
