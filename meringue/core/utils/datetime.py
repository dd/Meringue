import datetime as dt


__all__ = [
    "format_date_from_to",
]


def format_date_from_to(
    date_start: dt.date,
    date_end: dt.date,
    delimiter: str = "-",
) -> str:
    """
    Method to display date period.

    Possible output formats depending on the input data:

    * `DD.MM.YYYY - DD.MM.YYYY`
    * `DD.MM - DD.MM.YYYY`
    * `DD - DD.MM.YYYY`
    * `DD.MM.YYYY`

    Examples:
        ```pycon
        >>> print(format_date_from_to(dt.date(2020, 1, 1), dt.date(2020, 2, 1)))
        01.01 - 01.02.2020
        ```

    Attributes:
        date_start: Period start date.
        date_end: Period end date.
        delimiter: Dates delimiter.

    Returns:
        Date period string.
    """

    if date_start.year != date_end.year:
        return f"{date_start:%d.%m.%Y} {delimiter} {date_end:%d.%m.%Y}"

    if date_start.month != date_end.month:
        return f"{date_start:%d.%m} {delimiter} {date_end:%d.%m.%Y}"

    if date_start.day != date_end.day:
        return f"{date_start:%d} {delimiter} {date_end:%d.%m.%Y}"

    return f"{date_end:%d.%m.%Y}"
