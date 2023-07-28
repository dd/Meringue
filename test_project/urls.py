from django.urls import path

from meringue.core.views import im_a_teapot
from test_project.views import RegistrationView
from test_project.views import upload_file


urlpatterns = [
    path("make_coffee", im_a_teapot, name="make_coffee"),
    path("upload_file", upload_file, name="upload_file"),
    path("registration", RegistrationView.as_view(), name="registration"),
]
