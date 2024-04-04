from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView

from meringue.core.views import im_a_teapot
from meringue.protected.views import x_accel_redirect_view
from test_project.views import RegistrationView
from test_project.views import upload_file


urlpatterns = [
    path("make_coffee", im_a_teapot, name="make_coffee"),
    path("upload_file", upload_file, name="upload_file"),
    path("registration", RegistrationView.as_view(), name="registration"),
    path("token_obtain", TokenObtainPairView.as_view(), name="token_obtain"),
    path(
        "protected/<int:cid>/<slug:field>/<slug:pk>/<slug:disp>",
        x_accel_redirect_view,
        name="x_accel_redirect_view",
    ),
]
