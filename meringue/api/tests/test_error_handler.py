from unittest.mock import patch

from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.test import override_settings
from django.urls import reverse

import pytest
from rest_framework.exceptions import ErrorDetail
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIClient


@override_settings(REST_FRAMEWORK={"EXCEPTION_HANDLER": "meringue.api.handlers.exception_handler"})
@patch(
    "test_project.views.RegistrationView.post",
    autospec=True,
    side_effect=Exception("Checking for 500 errors"),
)
def test_500(mocked_post):
    """
    Checking for raise 500 errors
    """
    client = APIClient()
    with pytest.raises(Exception, match="Checking for 500 errors"):
        client.post(reverse("registration"), format="json")


@override_settings(REST_FRAMEWORK={"EXCEPTION_HANDLER": "meringue.api.handlers.exception_handler"})
def test_405():
    """
    Checking for raise 405 errors
    """
    client = APIClient()
    resp = client.get(reverse("registration"), format="json")
    assert resp.status_code == 405
    assert resp.json() == {"detail": 'Method "GET" not allowed.'}


@override_settings(REST_FRAMEWORK={"EXCEPTION_HANDLER": "meringue.api.handlers.exception_handler"})
@patch("test_project.views.RegistrationView.post", autospec=True, side_effect=Http404())
def test_404(mocked_post):
    """
    Checking for raise 404 errors
    """
    client = APIClient()
    resp = client.post(reverse("registration"), format="json")
    assert resp.status_code == 404
    assert resp.json() == {"detail": "Not found."}


@override_settings(REST_FRAMEWORK={"EXCEPTION_HANDLER": "meringue.api.handlers.exception_handler"})
@patch("test_project.views.RegistrationView.post", autospec=True, side_effect=PermissionDenied())
def test_403(mocked_post):
    """
    Checking for raise 403 errors
    """
    client = APIClient()
    resp = client.post(reverse("registration"), format="json")
    assert resp.status_code == 403
    assert resp.json() == {"detail": "You do not have permission to perform this action."}


@override_settings(REST_FRAMEWORK={"EXCEPTION_HANDLER": "meringue.api.handlers.exception_handler"})
def test_serializer_error():
    """
    Checking serializer error handling
    """
    client = APIClient()
    resp = client.post(reverse("registration"), format="json")
    assert resp.status_code == 400
    assert resp.json() == {"username": [{"message": "Обязательное поле.", "code": "required"}]}


@override_settings(REST_FRAMEWORK={"EXCEPTION_HANDLER": "meringue.api.handlers.exception_handler"})
@patch(
    "test_project.views.UserSerializer.is_valid",
    autospec=True,
    side_effect=ValidationError("Error message", "error_code"),
)
def test_validation_error(mocked_is_valid):
    """
    Checking single error validation handling
    """
    client = APIClient()
    resp = client.post(reverse("registration"), format="json")
    assert resp.status_code == 400
    assert resp.json() == [{"code": "error_code", "message": "Error message"}]


@override_settings(REST_FRAMEWORK={"EXCEPTION_HANDLER": "meringue.api.handlers.exception_handler"})
@patch(
    "test_project.views.UserSerializer.is_valid",
    autospec=True,
    side_effect=ValidationError(
        {
            "username": {"1": ErrorDetail("Error message", "error_code")},
        }
    ),
)
def test_validation_dict_error(mocked_is_valid):
    """
    Checking single error validation handling
    """
    client = APIClient()
    resp = client.post(reverse("registration"), format="json")
    assert resp.status_code == 400
    assert resp.json() == {"username": {"1": {"message": "Error message", "code": "error_code"}}}
