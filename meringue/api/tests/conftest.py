from django.contrib.auth.models import User

from rest_framework import mixins
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username",)


class UsersViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer

    @action(detail=False)
    def quantity(self, request, pk=None):
        qs = self.get_queryset()
        return Response({"quantity": qs.count()})

    @action(detail=True)
    def ping(self, request):
        return Response({"detail": "pong"})


class ProfileViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    serializer_class = ProfileSerializer
    m_object_detail = True

    def get_object(self):
        return User.objects.first()

    @action(detail=False)
    def ping(self, request):
        return Response({"detail": "pong"})
