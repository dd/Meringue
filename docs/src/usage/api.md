# Meringue Api

This is an application with a set of various utilities for the API and in particular for the [Django Rest Framework](https://www.django-rest-framework.org/).


## handlers

### exception_handler

Error handler for _django rest framework_.

This handler returns errors in the format of code and error message pairs, this can be useful when it is necessary to implement different behavior on the front depending on the type of error (for example, in a certain case, show a popup with extended information about the cause of the error).

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
