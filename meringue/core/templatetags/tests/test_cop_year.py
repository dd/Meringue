import datetime as dt
from unittest.mock import patch

from django.template import Context
from django.template import Template
from django.test import override_settings

import pytz


@override_settings(MERINGUE={"COP_YEAR": 2023})
@patch(
    "django.utils.timezone.localtime",
    return_value=dt.datetime(2023, 1, 1, 0, 0, 0, tzinfo=pytz.utc),
)
def test_with_current_year(mocked_localtime):
    """
    Tag validation when used with current year
    """

    t = Template("{% load meringue_base %}{% cop_year %}")
    string = t.render(Context())
    assert string == "2023"


@override_settings(MERINGUE={"COP_YEAR": 2000, "COP_YEARS_DIFF": 10})
@patch(
    "django.utils.timezone.localtime",
    return_value=dt.datetime(2023, 1, 1, 0, 0, 0, tzinfo=pytz.utc),
)
def test_range_of_years(mocked_localtime):
    """
    Using the tag in the case of a range of years
    """

    t = Template("{% load meringue_base %}{% cop_year %}")
    string = t.render(Context())
    assert string == "2000&mdash;2023"


@override_settings(MERINGUE={"COP_YEAR": 2020, "COP_YEARS_DIFF": 10})
@patch(
    "django.utils.timezone.localtime",
    return_value=dt.datetime(2023, 1, 1, 0, 0, 0, tzinfo=pytz.utc),
)
def test_years_difference(mocked_localtime):
    """
    Not much difference between years
    """

    t = Template("{% load meringue_base %}{% cop_year %}")
    string = t.render(Context())
    assert string == "2023"
