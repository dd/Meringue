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


## docs

When generating API documentation using [drf-spectacular](https://drf-spectacular.readthedocs.io/en/latest/), it is possible to intervene in the resulting object in a limited and inconvenient way:

* Firstly, it is proposed to do all this in the settings, which no longer implies a large amount of data (or it will be terribly inconvenient);
* Secondly, it is difficult to do some manipulations "on the fly" (for example, depending on the environment, you may have a different set of authorization methods, or something else);
* Thirdly, if you have several apexes and, accordingly, documentation, you will not be able to do, for example, a different description for different apexes / documentation.

To solve all these problems, we implemented a [patcher][openapischemapatcher] and a [view][meringuespectacularapiview] to load it.


### OpenAPISchemaPatcher

This is an OpenAPI3 schema patcher that makes it relatively easy to add data to the schema. Everything is quite simple and without much logic, just additional data is first registered, then the scheme is supplemented with them.

To register additional objects, there is the following set of methods:

#### register_security_scheme

::: meringue.api.docs.patchers.OpenAPISchemaPatcher.register_security_scheme
	options:
		show_root_heading: false
		show_root_toc_entry: false
		show_source: false
		show_docstring_raises: false

Example:

```python
from meringue.api.docs import OpenAPISchemaPatcher
patcher = OpenAPISchemaPatcher()
patcher.register_security_scheme("name", { ... })
```

#### register_component_scheme

::: meringue.api.docs.patchers.OpenAPISchemaPatcher.register_component_scheme
	options:
		show_root_heading: false
		show_root_toc_entry: false
		show_source: false
		show_docstring_raises: false

Example:

```python
from meringue.api.docs import OpenAPISchemaPatcher
patcher = OpenAPISchemaPatcher()
patcher.register_component_scheme("name", { ... })
```

#### register_tag

::: meringue.api.docs.patchers.OpenAPISchemaPatcher.register_tag
	options:
		show_root_heading: false
		show_root_toc_entry: false
		show_source: false
		show_docstring_raises: false

Example:

```python
from meringue.api.docs import OpenAPISchemaPatcher
patcher = OpenAPISchemaPatcher()
patcher.register_tag({
   "name": "meringue",
   "x-displayName": "Meringue",
})
```

#### patch_description

::: meringue.api.docs.patchers.OpenAPISchemaPatcher.patch_description
	options:
		show_root_heading: false
		show_root_toc_entry: false
		show_source: false
		show_docstring_raises: false

Example:

```pycon
>>> from meringue.api.docs import OpenAPISchemaPatcher
>>> patcher = OpenAPISchemaPatcher()
>>> schema = {
...     "servers": [
...         {
...             "description": "Server 1",
...             "url": "https://example-1.com",
...         },
...         {
...             "description": "Server 2",
...             "url": "example-2.com",
...         },
...     ],
...     "info": {
...         "description": "Test API",
...     },
... }
>>> patcher.patch_description(schema)
>>> print(schema)
{
    "servers": [
        {
            "description": "Server 1",
            "url": "https://example-1.com",
        },
        {
            "description": "Server 2",
            "url": "example-2.com",
        },
    ],
    "info": {
        "description": "Test API\n\nServer 1 API [example-1.com](https://example-1.com)\n\nServer 2 API [example-2.com](example-2.com)",
    },
}
```

#### patch_security_schemes

::: meringue.api.docs.patchers.OpenAPISchemaPatcher.patch_security_schemes
	options:
		show_root_heading: false
		show_root_toc_entry: false
		show_source: false
		show_docstring_raises: false

Example:

```pycon
>>> from meringue.api.docs import OpenAPISchemaPatcher
>>> patcher = OpenAPISchemaPatcher()
>>> patcher.register_security_scheme("name", { ... })
>>> schema = {}
>>> patcher.patch_security_schemes(schema)
>>> print(schema)
{
    "components": {
        "securitySchemes": {
            "name": { ... },
        },
    },
}
```

#### patch_component_schemes

::: meringue.api.docs.patchers.OpenAPISchemaPatcher.patch_component_schemes
	options:
		show_root_heading: false
		show_root_toc_entry: false
		show_source: false
		show_docstring_raises: false

Example:

```pycon
>>> from meringue.api.docs import OpenAPISchemaPatcher
>>> patcher = OpenAPISchemaPatcher()
>>> patcher.register_component_scheme("name", { ... })
>>> schema = {}
>>> patcher.patch_component_schemes(schema)
>>> print(schema)
{
    "components": {
        "schemas": {
            "name": { ... },
        },
    },
}
```

#### patch_tags

::: meringue.api.docs.patchers.OpenAPISchemaPatcher.patch_tags
	options:
		show_root_heading: false
		show_root_toc_entry: false
		show_source: false
		show_docstring_raises: false

Example:

```pycon
>>> from meringue.api.docs import OpenAPISchemaPatcher
>>> schema = {
...     "servers": [
...         {
...             "description": "Server 1",
...             "url": "https://example-1.com",
...         },
...         {
...             "description": "Server 2",
...             "url": "example-2.com",
...         },
...     ],
... }
>>> patcher = OpenAPISchemaPatcher()
>>> patcher.register_tag({
...    "name": "meringue",
...    "x-displayName": "Meringue",
... })
>>> patcher.patch_tags(schema)
>>> print(schema)
{
    "servers": [
        {
            "description": "Server 1",
            "url": "https://example-1.com",
        },
        {
            "description": "Server 2",
            "url": "example-2.com",
        },
    ],
    "tags": [
            {
            "name": "meringue",
            "x-displayName": "Meringue",
        },
    ],
}
```

#### patch_schema

::: meringue.api.docs.patchers.OpenAPISchemaPatcher.patch_schema
	options:
		show_root_heading: false
		show_root_toc_entry: false
		show_source: false
		show_docstring_raises: false


### MeringueSpectacularAPIView

This view is a wrapper around the original [SpectacularAPIView](drf_spectacular.views.SpectacularAPIView), but with the addition of a method that patches the OpenAPI schema.

```python title="urls.py"
from django.urls import path

from meringue.api.docs import OpenAPISchemaPatcher
from meringue.api.docs import MeringueSpectacularAPIView


patcher = OpenAPISchemaPatcher()
patcher.register_tag({
   "name": "meringue",
   "x-displayName": "Meringue",
})

urlpatterns = [
    path("schema", MeringueSpectacularAPIView.as_view(patcher=patcher), name="schema"),
]
```
