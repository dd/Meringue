import datetime as dt

from meringue.core.utils.datetime import format_date_from_to


def test_different_dates():
    """
    Validating a tag with two completely different dates.
    """

    result = format_date_from_to(
        date_start=dt.date(2021, 1, 1),
        date_end=dt.date(2023, 1, 1),
        delimiter="-",
    )
    assert result == "01.01.2021 - 01.01.2023"


def test_same_year():
    """
    Tag validation for same years.
    """

    result = format_date_from_to(
        date_start=dt.date(2023, 1, 1),
        date_end=dt.date(2023, 4, 1),
        delimiter="-",
    )
    assert result == "01.01 - 01.04.2023"


def test_same_month():
    """
    Checking a tag for a period with a difference of a month.
    """

    result = format_date_from_to(
        date_start=dt.date(2023, 1, 1),
        date_end=dt.date(2023, 1, 4),
        delimiter="-",
    )
    assert result == "01 - 04.01.2023"


def test_same_dates():
    """
    Tag validation for same dates.
    """

    result = format_date_from_to(
        date_start=dt.date(2023, 1, 1),
        date_end=dt.date(2023, 1, 1),
        delimiter="-",
    )
    assert result == "01.01.2023"


def test_delimiter():
    """
    Delimiter Change Check.
    """

    result = format_date_from_to(
        date_start=dt.date(2021, 1, 1),
        date_end=dt.date(2023, 4, 1),
        delimiter="to",
    )
    assert result == "01.01.2021 to 01.04.2023"
