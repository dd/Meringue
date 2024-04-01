from django.core.exceptions import PermissionDenied
from django.http.response import Http404

from rest_framework import exceptions
from rest_framework import views

from meringue.api.utils import render_error_details

try:
    from rest_framework_simplejwt.exceptions import DetailDictMixin
except ImportError:
    DetailDictMixin = None


def exception_handler(exc, context):
    """
    Error handler returning message and error code pairs.

    The handler is a wrapper over the standard handler `rest_framework.views.exception_handler`.
    """

    response = views.exception_handler(exc, context)

    if response is None:
        return response

    if isinstance(exc, (Http404, PermissionDenied)):
        # django Http404 and PermissionDenied errors are substituted for drf errors,
        # in `rest_framework.views.exception_handler` method.
        response.data = render_error_details(response.data["detail"])

    elif DetailDictMixin and isinstance(exc, DetailDictMixin):
        response.data = render_error_details(exc)

    elif isinstance(exc, exceptions.APIException):
        response.data = render_error_details(exc.detail)

    return response
