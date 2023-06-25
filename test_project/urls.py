from django.urls import path

from meringue.core.views import im_a_teapot


urlpatterns = [
    path("make_coffee", im_a_teapot, name="make_coffee"),
]
