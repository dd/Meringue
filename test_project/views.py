from django.http import HttpResponseBadRequest
from django.http import JsonResponse


def upload_file(request):
    if "file" in request.FILES:
        return JsonResponse({"file": request.FILES["file"].name})

    raise HttpResponseBadRequest()
