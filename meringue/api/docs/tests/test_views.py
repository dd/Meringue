from unittest.mock import patch

from django.test import Client
from django.test import override_settings
from django.urls import include
from django.urls import path
from django.urls import reverse

from rest_framework.routers import DefaultRouter

from meringue.api.docs import MeringueSpectacularAPIView
from meringue.api.docs import OpenAPISchemaPatcher


@patch.object(OpenAPISchemaPatcher, "patch_schema")
def test_get_schema(mocked_patch_schema):
    """
    Checking registered routes
    """

    router = DefaultRouter()
    patcher = OpenAPISchemaPatcher()

    class TempUrls:
        urlpatterns = [
            path("schema", MeringueSpectacularAPIView.as_view(patcher=patcher), name="schema"),
            path("", include(router.urls)),
        ]

    client = Client()
    with override_settings(ROOT_URLCONF=TempUrls):
        response = client.get(reverse("schema"))
        assert response.status_code == 200

    mocked_patch_schema.assert_called_once()


def test_get_schema_without_patcher():
    """
    Checking registered routes
    """

    router = DefaultRouter()

    class TempUrls:
        urlpatterns = [
            path("schema", MeringueSpectacularAPIView.as_view(), name="schema"),
            path("", include(router.urls)),
        ]

    client = Client()
    with override_settings(ROOT_URLCONF=TempUrls):
        response = client.get(reverse("schema"))
        assert response.status_code == 200
