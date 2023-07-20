# Meringue Api

This is an application with a set of various utilities for the API and in particular for the [Django Rest Framework](https://www.django-rest-framework.org/).


## routers

### MeringueRouter

It's a _django rest framework_ router, with some additional specific functionality.

#### Root view

The router enables and disables the root view according to the [API_ENABLE_ROOT_VIEW][meringue.conf.default_settings.API_ENABLE_ROOT_VIEW] setting. By default, the parameter corresponds to the value of the **DEBUG** parameter and in production the root view is disabled.

#### Object predefined detail route

The router allows you to add **ViewSet** for predefined objects - that is, a _ViewSet_ object for which it is known in advance, the simplest example is a profile. To manage a profile, it is often necessary to have a set of views - getting a profile, editing, deleting. The default behavior of _DRF_ will either require you to use an id to request a profile, or make several separate views for this, this router allows you to use _ViewSet_ for this. To implement such a _ViewSet_, you need to make a standard _ViewSet_ and specify the flag `m_object_detail = True`.

For example, _ViewSet_ for a profile in general will look like this:

```py hl_lines="9"
class ProfileViewSet(
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    permission_classes = (ProfilePermission, )
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    object_detail = True

    def get_object(self):
        user = self.request.user
        self.check_object_permissions(self.request, user)
        return user

    def perform_destroy(self, instance):
        self.request.user = AnonymousUser()
        super().perform_destroy(instance)
```

Of course, for such a router, it will not work to use `ListModelMixin`.

The router itself in use is exactly the same as a regular one:

```py
from meringue.api.routers import MeringueRouter

router = MeringueRouter()
router.register('profile', ProfileViewSet, basename="profile")

urlpatterns = [
    path('', include(router.urls)),
]
```


## handlers

### exception_handler

Error handler for _django rest framework_.

This handler returns errors in the format of code and error message pairs, this can be useful when it is necessary to implement different behavior on the front depending on the type of error (for example, in a certain case, show a popup with extended information about the cause of the error).

```py title="settings.py"
REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "meringue.api.handlers.exception_handler",
}
```

```pycon
>>> from rest_framework import serializers
>>> from django.contrib.auth.models import User

>>> class UserSerializer(serializers.ModelSerializer):
>>>     class Meta:
>>>         model = User
>>>         fields = ["username",]

>>> serializer = UserSerializer(data={})
>>> serializer.is_valid()
>>> print(serializer.errors)
{'username': [ErrorDetail(string='Required field.', code='required')]}
```
