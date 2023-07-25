# Meringue Api

Это приложение с набором разнообразных утилит для работы API и в частности для [Django Rest Framework](https://www.django-rest-framework.org/).


## routers

### MeringueRouter

Это _django rest framework_ роутер, с некоторым дополнительным специфическим функционалом.

#### Root view

В роутере включается и выключается корневое представление в соответствии с параметром [API_ENABLE_ROOT_VIEW][meringue.conf.default_settings.API_ENABLE_ROOT_VIEW]. По умолчанию параметр соответствует значению параметра **DEBUG** и в продакшене корневое представление отключено.

#### Object predefined detail route

Роутер позволяет добавить **ViewSet** для предопределённых объектов - то есть _ViewSet_ объект для которого заранее известен, самый простой пример это профиль. Для управления профилем часто необходимо иметь набор представлений - получение профиля, редактирование, удаление. Стандартное поведение _DRF_ потребует либо использовать id для запроса профиля, либо делать несколько отдельных view для этого, данный роутер позволяет для этого использовать _ViewSet_. Что бы реализоватаь такой _ViewSet_ необходимо сделать стандартный _ViewSet_ и указать у него флаг `m_object_detail = True`.

Например _ViewSet_ для профиля в общем виде будет выглядеть следующим образом:

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

Само собой для такого роутера не получится использовать `ListModelMixin`.

Сам роутер в использовании точно такой же как и обычный:

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

Обработчик ошибок для _django rest framework_.

Данный обработчик возвращает ошибки в формате пар код и сообщение ошибки, это может быть полезно когда на фронте необходимо реализовать разное поведение в зависимости от типа ошибки (например в определённом случае показать попап с расширенной информацией о причине ошибке).

```py title="settings.py"
MERINGUE = {
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

При генерации документации апишки с использованием [drf-spectacular](https://drf-spectacular.readthedocs.io/en/latest/), вмешаться в полученый объект можно ограниченно и неудобно:

* Во-первых, предлагается всё это делать в настройках, что уже не предполагает большого объёма данных (либо это будет жутко неудобно);
* Во вторых, сложно сделать какие-то манипуляции "на лету" (например в зависимости от окружения, у вас может отличаться набор способов авторизаций, или ещё что-нибудь)
* В третьих, если у вас несколько апишек и соответственно, документаций, у вас не получиться сделать, например, разное описание для разных апишек / документаций.

Чтобы решить все эти проблемы мы реализовали [патчер][openapischemapatcher] и в нагрузку к нему [представление][meringuespectacularapiview].


### OpenAPISchemaPatcher

Это патчер схемы OpenAPI3, с помощью которого можно относительно просто дополнить схему нужными данным. Всё довольно простот и без особой логики, просто сначала регистрируется дополнительные данные, потом ими дополняется схема.

Чтобы зарегистрировать дополнительные объекты есть следующий набор методов:

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

Это представление обёртка вокруг оригинального представления [SpectacularAPIView][drf_spectacular.views.SpectacularAPIView], но с добавлением метода который патчит схему OpenAPI.

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

