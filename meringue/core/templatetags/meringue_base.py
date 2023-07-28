import datetime as dt

from django import template
from django.utils import timezone
from django.utils.safestring import mark_safe

from meringue.conf import m_settings
from meringue.core.utils import format_date_from_to


register = template.Library()


@register.simple_tag
def cop_year() -> str:
    """
    A tag that displays the year or range of years for the copyright string in `YYYY-YYYY` format.

    Examples:
        ```jinja
        <p>Copyright © {% cop_year %} My company</p>
        ```

    Raises:
        Exception: To use the `cop_year` tag, you must fill in the `COP_YEAR` parameter in the
            meringue settings

    Returns:
        Year for copyrights.
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
def date_range(date_start: dt.date, date_end: dt.date) -> str:
    """
    Return range of date in one of the following formats:

    * `DD.MM.YYYY - DD.MM.YYYY`
    * `DD.MM - DD.MM.YYYY`
    * `DD - DD.MM.YYYY`
    * `DD.MM.YYYY`

    Attributes:
        date_start: Period start date.
        date_end: Period end date.

    Examples:
        ```jinja
        {% date_range date_start date_end %}
        ```

    Returns:
        Date period.
    """

    tmp_result = format_date_from_to(date_start, date_end, "-")

    if date_start == date_end:
        return tmp_result

    tmp_date_start, tmp_date_end = tmp_result.split(" - ")

    return mark_safe(f"{tmp_date_start}&nbsp;&mdash; {tmp_date_end}")  # noqa: S308
