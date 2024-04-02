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


def protected_file_view(request, cid, field, pk):
    """
    В продакшен моде вьха редиректит на урл файла, где нжинкс отдаёт этот файл
    Защита работает за счёт параметра internal
    https://nginx.org/en/docs/http/ngx_http_core_module.html#internal

    ```conf
    location /media/protected/ {
        internal;
        alias /home/rpl/rpl-2023-back/public/media/protected/;
    }
    ```
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
        response["Content-Disposition"] = f"inline; filename={quote(file_name)}"

        if isinstance(file, ProtectedFieldFile | ProtectedImageFieldFile):
            redirect_url = file.original_url
        else:
            redirect_url = file.url

        response["X-Accel-Redirect"] = redirect_url
        return response

    return FileResponse(open(file.path, "rb"))
