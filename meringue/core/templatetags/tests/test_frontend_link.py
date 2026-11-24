from django.template import Context
from django.template import Template
from django.test import override_settings


@override_settings(
    MERINGUE={"FRONTEND_URLS": {"index": "/"}, "FRONTEND_DOMAIN": "https://example.com"},
)
def test_absolute_link():
    """Render an absolute frontend URL by default."""
    template = Template("{% load meringue_base %}{% frontend_link 'index' %}")

    assert template.render(Context()) == "https://example.com/"


@override_settings(MERINGUE={"FRONTEND_URLS": {"user": "/user/{id}"}})
def test_relative_link_with_params():
    """Render a relative URL with a context parameter and no frontend domain."""
    template = Template(
        "{% load meringue_base %}{% frontend_link 'user' absolute=False id=user_id %}"
    )

    assert template.render(Context({"user_id": 123})) == "/user/123"


@override_settings(
    MERINGUE={
        "FRONTEND_URLS": {"user": lambda user_id: f"/user/{user_id}"},
        "FRONTEND_DOMAIN": "https://example.com",
    },
)
def test_callable_link_with_params():
    """Pass template parameters to a callable frontend URL."""
    template = Template("{% load meringue_base %}{% frontend_link 'user' user_id=user_id %}")

    assert template.render(Context({"user_id": 123})) == "https://example.com/user/123"


@override_settings(
    MERINGUE={"FRONTEND_URLS": {"index": "/"}, "FRONTEND_DOMAIN": "https://example.com"},
)
def test_assign_link():
    """Assign the URL to a context variable without rendering it immediately."""
    template = Template("{% load meringue_base %}{% frontend_link 'index' as link %}[{{ link }}]")

    assert template.render(Context()) == "[https://example.com/]"


@override_settings(
    MERINGUE={
        "FRONTEND_URLS": {"search": "/search?q={query}&page=1"},
        "FRONTEND_DOMAIN": "https://example.com",
    },
)
def test_escape_link():
    """Escape query string separators and quotes when rendering a URL in HTML."""
    template = Template("{% load meringue_base %}{% frontend_link 'search' query=query %}")

    assert (
        template.render(Context({"query": '"example"'}))
        == "https://example.com/search?q=&quot;example&quot;&amp;page=1"
    )
