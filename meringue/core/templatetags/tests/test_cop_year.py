import datetime as dt
from unittest.mock import patch

from django.template import Context
from django.template import Template
from django.test import override_settings

import pytest
import pytz


@override_settings(MERINGUE={"COP_YEAR": 2023})
@patch(
    "django.utils.timezone.localtime",
    return_value=dt.datetime(2023, 1, 1, 0, 0, 0, tzinfo=pytz.utc),
)
def test_with_current_year(mocked_localtime):
    """
    Tag validation when used with current year.
    """

    t = Template("{% load meringue_base %}{% cop_year %}")
    render = t.render(Context())
    assert render == "2023"


@override_settings(MERINGUE={"COP_YEAR": 2000, "COP_YEARS_DIFF": 10})
@patch(
    "django.utils.timezone.localtime",
    return_value=dt.datetime(2023, 1, 1, 0, 0, 0, tzinfo=pytz.utc),
)
def test_range_of_years(mocked_localtime):
    """
    Using the tag in the case of a range of years.
    """

    t = Template("{% load meringue_base %}{% cop_year %}")
    render = t.render(Context())
    assert render == "2000&mdash;2023"


@override_settings(MERINGUE={"COP_YEAR": 2020, "COP_YEARS_DIFF": 10})
@patch(
    "django.utils.timezone.localtime",
    return_value=dt.datetime(2023, 1, 1, 0, 0, 0, tzinfo=pytz.utc),
)
def test_years_difference(mocked_localtime):
    """
    Not much difference between years.
    """

    t = Template("{% load meringue_base %}{% cop_year %}")
    render = t.render(Context())
    assert render == "2023"


@override_settings(MERINGUE={})
def test_not_specified_setting():
    """
    Error checking if do not specify `COP_YEAR` in the settings.
    """

    t = Template("{% load meringue_base %}{% cop_year %}")

    msg = (
        "To use the `cop_year` tag, you must fill in the `COP_YEAR` parameter in the meringue "
        "settings"
    )
    with pytest.raises(Exception, match=msg):
        t.render(Context())
