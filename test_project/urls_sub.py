from django.urls import path

from meringue.protected.views import protected_file_view


urlpatterns = [
    path(
        "protected/<int:cid>/<slug:field>/<slug:pk>",
        protected_file_view,
        name="meringue-protected-file",
    ),
]
