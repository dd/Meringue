from django import template
from django.utils import timezone
from django.utils.safestring import mark_safe

from meringue.conf import m_settings


register = template.Library()


@register.simple_tag
def cop_year():
    """
    A tag that displays the year or range of years for the copyright string in YYYY-YYYY format.

    Examples:
        ```jinja
        <p>Copyright © {% cop_year %} My company</p>
        ```

    For the tag to work, you must fill in the `COP_YEAR` parameter in the settings.
    """

    if m_settings.COP_YEAR is None:
        msg = (
            "To use the `cop_year` tag, you must fill in the `COP_YEAR` parameter in the "
            "meringue settings"
        )
        raise Exception(msg)

    year = timezone.localtime().year

    if year == m_settings.COP_YEAR or year - m_settings.COP_YEAR < m_settings.COP_YEARS_DIFF:
        return year

    return mark_safe(f"{m_settings.COP_YEAR}&mdash;{year}")  # noqa: S308


@register.simple_tag
def date_range(date_start, date_end):
    """
    return range of date in one of the following formats:
        DD MM YYYY - DD MM YYYY
        DD MM - DD MM YYYY
        DD - DD MM YYYY
    """

    if date_start.year != date_end.year:
        result = "&nbsp;&mdash; ".join(
            [date_start.strftime("%d %B %Y"), date_end.strftime("%d %B %Y")],
        )
    elif date_start.month != date_end.month:
        result = "&nbsp;&mdash; ".join(
            [date_start.strftime("%d %B"), date_end.strftime("%d %B %Y")],
        )
    elif date_start.day != date_end.day:
        result = "&mdash;".join(
            [date_start.strftime("<nobr>%d"), date_end.strftime("%d %B</nobr> %Y")],
        )
    else:
        result = date_end.strftime("%d %B %Y")

    return mark_safe(result)  # noqa: S308
