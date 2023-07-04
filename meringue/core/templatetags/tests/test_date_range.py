import datetime as dt

from django.template import Context
from django.template import Template


def test_different_dates():
    """
    Validating a tag with two completely different dates.
    """

    t = Template("{% load meringue_base %}{% date_range date_start date_end %}")
    c = Context(
        {
            "date_start": dt.date(2021, 1, 1),
            "date_end": dt.date(2023, 1, 1),
        }
    )
    render = t.render(c)
    assert render == "01.01.2021&nbsp;&mdash; 01.01.2023"


def test_same_year():
    """
    Tag validation for same years.
    """

    t = Template("{% load meringue_base %}{% date_range date_start date_end %}")
    c = Context(
        {
            "date_start": dt.date(2023, 1, 1),
            "date_end": dt.date(2023, 4, 1),
        }
    )
    render = t.render(c)
    assert render == "01.01&nbsp;&mdash; 01.04.2023"


def test_same_month():
    """
    Checking a tag for a period with a difference of a month.
    """

    t = Template("{% load meringue_base %}{% date_range date_start date_end %}")
    c = Context(
        {
            "date_start": dt.date(2023, 1, 1),
            "date_end": dt.date(2023, 1, 4),
        }
    )
    render = t.render(c)
    assert render == "01&nbsp;&mdash; 04.01.2023"


def test_same_dates():
    """
    Tag validation for same dates.
    """

    t = Template("{% load meringue_base %}{% date_range date_start date_end %}")
    c = Context(
        {
            "date_start": dt.date(2023, 1, 1),
            "date_end": dt.date(2023, 1, 1),
        }
    )
    render = t.render(c)
    assert render == "01.01.2023"
