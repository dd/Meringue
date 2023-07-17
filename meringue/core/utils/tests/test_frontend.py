from django.test import override_settings

import pytest

from meringue.core.utils.frontend import get_link


@override_settings(
    MERINGUE={"FRONTEND_URLS": {"foo": "/"}, "FRONTEND_DOMAIN": "https://example.com"},
)
def test_get_link():
    """
    Checking for getting a regular link
    """
    link = get_link("foo")
    assert link == "https://example.com/"


@override_settings(
    MERINGUE={
        "FRONTEND_URLS": {"foo": "/foo/{bar}/{baz}"},
        "FRONTEND_DOMAIN": "https://example.com",
    },
)
def test_with_params():
    """
    Checking for getting a link with parameters
    """
    link = get_link("foo", bar="bar", baz=1)
    assert link == "https://example.com/foo/bar/1"


@override_settings(
    MERINGUE={
        "FRONTEND_URLS": {"foo": lambda bar: f"/foo?param={bar}"},
        "FRONTEND_DOMAIN": "https://example.com",
    },
)
def test_callable_link():
    """
    Checking for getting a link with callable link
    """
    link = get_link("foo", bar="bar")
    assert link == "https://example.com/foo?param=bar"


@override_settings(
    MERINGUE={"FRONTEND_URLS": {"foo": "/foo"}},
)
def test_without_domain():
    """
    Checking for getting a link without domain
    """

    link = get_link("foo", False)
    assert link == "/foo"


@override_settings(
    MERINGUE={
        "FRONTEND_URLS": {
            "foo": "/foo",
            "bar": "bar",
        },
        "FRONTEND_DOMAIN": "https://example.com",
    },
)
def test_final_link():
    """
    Checking the formation of the final link

    Given two links, one with a slash, the second without, check the generated links.
    """

    foo_link = get_link("foo")
    bar_link = get_link("bar")
    assert foo_link == "https://example.com/foo"
    assert bar_link == "https://example.com/bar"


@override_settings(MERINGUE={})
def test_not_set_settings_param():
    """
    Check return error due to not specifying a dict of links
    """

    msg = "FRONTEND_URLS parameter is empty"
    with pytest.raises(Exception, match=msg):
        get_link("foo")


@override_settings(MERINGUE={"FRONTEND_URLS": {"foo": "/foo"}})
def test_has_no_link():
    """
    Checking the return of an error, the absence of the requested link in the list
    """

    msg = "The passed link `bar` is not specified in the FRONTEND_URLS parameter"
    with pytest.raises(Exception, match=msg):
        get_link("bar")


@override_settings(MERINGUE={"FRONTEND_URLS": {"foo": "/foo"}})
def test_not_set_domain():
    """
    Check return error when no domain is specified
    """

    msg = "FRONTEND_DOMAIN option not set"
    with pytest.raises(Exception, match=msg):
        get_link("foo")
