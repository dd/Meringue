import mimetypes
from pathlib import Path
from urllib.parse import quote
from urllib.parse import urljoin

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.http import FileResponse
from django.http import Http404
from django.http import HttpResponse

from meringue.conf import m_settings
from meringue.protected.fields import ProtectedFieldFile
from meringue.protected.fields import ProtectedImageFieldFile


def x_accel_redirect_view(request, cid, field, pk, disp="inline"):
    """
    The view checks the user's access to view and serves the file.

    If you enable the parameter
    [PROTECTED_SERVE_WITH_NGINX][meringue.conf.default_settings.PROTECTED_SERVE_WITH_NGINX], the
    file will not be served; instead, the response will contain the X-Accel-Redirect header
    pointing to the original file. It is expected that nginx will return the file using the
    [internal](https://nginx.org/en/docs/http/ngx_http_core_module.html#internal) parameter.
    """

    contenttype = ContentType.objects.get(id=cid)

    if not request.user.has_perm(f"{contenttype.app_label}.view_{contenttype.model}"):
        raise PermissionDenied()

    model = contenttype.model_class().objects.get(pk=pk)
    file = getattr(model, field)

    if not file:
        raise Http404()

    if m_settings.PROTECTED_SERVE_WITH_NGINX:
        file_name = Path(file.name).name
        response = HttpResponse()
        response["Content-Type"] = mimetypes.guess_type(file.path)[0]
        response["Content-Disposition"] = f"{disp}; filename={quote(file_name)}"

        if isinstance(file, ProtectedFieldFile | ProtectedImageFieldFile):
            redirect_url = file.redirect_url
        else:
            redirect_url = file.url

        response["X-Accel-Redirect"] = redirect_url
        return response

    return FileResponse(
        open(file.path, "rb"),
        as_attachment = disp == "attachment",
    )
