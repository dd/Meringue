from rest_framework import exceptions
from rest_framework import views

from meringue.api.utils import render_error_details


def exception_handler(exc, context):
    """
    Error handler returning message and error code pairs.

    The handler is a wrapper over the standard handler `rest_framework.views.exception_handler`.
    """
    response = views.exception_handler(exc, context)

    if response is None:
        return response

    if isinstance(exc, exceptions.APIException):
        if isinstance(exc.detail, list):
            response.data = [render_error_details(e) for e in exc.detail]

        elif isinstance(exc.detail, dict):
            response.data = {f: render_error_details(e) for f, e in exc.detail.items()}

    return response
