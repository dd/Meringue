# -*- coding: utf-8 -*-

from django.http import HttpResponse


def im_a_teapot(request):
    return HttpResponse(status=418)
