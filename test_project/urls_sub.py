from django.urls import path

from meringue.protected.views import x_accel_redirect_view


urlpatterns = [
    path(
        "protected/<int:cid>/<slug:field>/<slug:pk>/<slug:disp>",
        x_accel_redirect_view,
        name="sub-x_accel_redirect_view",
    ),
]
