from django.contrib.auth.models import User
from django.http import HttpResponseBadRequest
from django.http import JsonResponse

from rest_framework import generics
from rest_framework import serializers


def upload_file(request):
    if "file" in request.FILES:
        return JsonResponse({"file": request.FILES["file"].name})

    raise HttpResponseBadRequest()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
        ]


class RegistrationView(generics.CreateAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = UserSerializer
