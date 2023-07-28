from django.test import override_settings
from django.urls import reverse

from rest_framework.test import APIClient

from meringue.api.routers import MeringueRouter
from meringue.api.tests.conftest import ProfileViewSet
from meringue.api.tests.conftest import UsersViewSet


def test_registered_routes():
    """
    Checking registered routes
    """

    router = MeringueRouter()
    router.register("profile", ProfileViewSet, basename="profile")
    router.register("friends", UsersViewSet, basename="friends")

    routes = [r.name for r in router.urls]
    expected_routes = [
        "profile",
        "profile",  # with format
        "profile-ping",
        "profile-ping",  # with format
        "friends-list",
        "friends-list",  # with format
        "friends-quantity",
        "friends-quantity",  # with format
        "friends-detail",
        "friends-detail",  # with format
        "friends-ping",
        "friends-ping",  # with format
    ]
    assert routes == expected_routes


def test_enable_root_view_param():
    """
    Checking the enable root view option
    """

    with override_settings(MERINGUE={"API_ENABLE_ROOT_VIEW": False}):
        router = MeringueRouter()
        assert router.urls == []

    with override_settings(MERINGUE={"API_ENABLE_ROOT_VIEW": True}):
        router = MeringueRouter()
        routes = [r.name for r in router.urls]
        assert routes == [
            "index",
            "index",  # with format
        ]


@override_settings(MERINGUE={"API_ENABLE_ROOT_VIEW": True})
def test_root_view_response():
    """
    Checking the list of routes returned by the root route
    """

    router = MeringueRouter()
    router.register("profile", ProfileViewSet, basename="profile")
    router.register("friends", UsersViewSet, basename="friends")

    class TempUrls:
        urlpatterns = router.urls

    expected_response = {
        "profile": "http://testserver/profile/",
        "friends": "http://testserver/friends/",
    }

    client = APIClient()
    with override_settings(ROOT_URLCONF=TempUrls):
        response = client.get(reverse("index"), format="json")
        assert response.json() == expected_response
