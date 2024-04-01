from rest_framework.exceptions import ErrorDetail

try:
    from rest_framework_simplejwt.exceptions import DetailDictMixin
except ImportError:
    DetailDictMixin = None


def render_error_details(error_detail: list | dict | ErrorDetail) -> list | dict:
    """
    The method renders errors of the ErrorDetail format into message and code pairs.

    Attributes:
        error_detail: Errors.

    Raises:
        Exception: Unknown error type.

    Returns:
        Rendered errors.
    """

    if DetailDictMixin and isinstance(error_detail, DetailDictMixin):
        return {
            "message": error_detail.detail["detail"],
            "code": error_detail.detail["code"],
        }

    elif isinstance(error_detail, list):
        error_list = [render_error_details(e) for e in error_detail]
        return error_list

    elif isinstance(error_detail, ErrorDetail):
        return {
            "message": str(error_detail),
            "code": error_detail.code,
        }

    elif isinstance(error_detail, dict):
        error_dict = {f: render_error_details(e) for f, e in error_detail.items()}
        return error_dict

    msg = f"Unknown error type {error_detail.__class__}: `{error_detail}`"
    raise Exception(msg)
