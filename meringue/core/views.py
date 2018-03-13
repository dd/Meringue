# -*- coding: utf-8 -*-

from django.http import HttpResponse


def im_a_teapot(request):
    """
    Most important functional
    """
    return HttpResponse(status=418)
