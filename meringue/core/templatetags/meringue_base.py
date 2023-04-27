# -*- coding: utf-8 -*-

from django import template
from django.utils import timezone
from django.utils.safestring import mark_safe

from meringue.conf import settings


register = template.Library()


@register.simple_tag
def cop_year():
    """
    return range of years for copyright in one of the following formats:
        YYYY-YYYY
        YYYY

    set start year for parametr MERINGUE_START_YEAR in setting.py
    """

    year = timezone.now().year
    return year == settings.START_YEAR and year or \
        mark_safe('%d&mdash;%d' % (settings.START_YEAR, year))


@register.simple_tag
def date_range(date_start, date_end):
    """
    return range of date in one of the following formats:
        DD MM YYYY - DD MM YYYY
        DD MM - DD MM YYYY
        DD - DD MM YYYY
    """

    if date_start.year != date_end.year:
        result = '&nbsp;&mdash; '.join([date_start.strftime('%d %B %Y'),
                                        date_end.strftime('%d %B %Y')])
    elif date_start.month != date_end.month:
        result = '&nbsp;&mdash; '.join([date_start.strftime('%d %B'),
                                        date_end.strftime('%d %B %Y')])
    elif date_start.day != date_end.day:
        result = '&mdash;'.join([date_start.strftime('<nobr>%d'),
                                 date_end.strftime('%d %B</nobr> %Y')])
    else:
        result = date_end.strftime('%d %B %Y')

    return mark_safe(result)
