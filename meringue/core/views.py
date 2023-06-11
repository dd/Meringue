from django.http import HttpResponse


def im_a_teapot(request):
    """
    Most important functional.

    Examples:
        ```py title="urls.py"
        from django.urls import path
        from meringue.core.views import im_a_teapot

        urlpatterns = [
            path('make_coffee', im_a_teapot, name="make_coffee"),
        ]
        ```
    """
    return HttpResponse(status=418)
