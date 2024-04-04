# Meringue Protected

This package includes functionality for organizing private files.

The main functionality is encapsulated in [x_accel_redirect_views][meringue.protected.views.x_accel_redirect_views]. It checks whether the user has access to view the file and serves it.

However, when working with nginx, you can enable the [PROTECTED_SERVE_WITH_NGINX][meringue.conf.default_settings.PROTECTED_SERVE_WITH_NGINX] option. In this case, nginx itself will serve the file instead of Django, using the [internal](https://nginx.org/en/docs/http/ngx_http_core_module.html#internal) directive.


## Usage

In the simplest scenario, you just need to enable view, and everything will work:

```python
urlpatterns = [
    ...
    path(
        "protected/<int:cid>/<slug:field>/<slug:pk>",
        staff_member_required(x_accel_redirect_views),
        name="meringue-protected-file",
    ),
    ...
]
```


### Nginx

Of course, when using nginx, files in the media folder need to be protected from access:

```conf
server {
    ...
    location /media/protected/ {
        return 404;
    }
    ...
}
```

However, for production, you can configure nginx to serve files instead of Django. To do this, you need to enable the [PROTECTED_SERVE_WITH_NGINX][meringue.conf.default_settings.PROTECTED_SERVE_WITH_NGINX] option and configure nginx as follows:

```conf
server {
    ...
    location /media/protected/ {
        internal;
        alias /home/user/public/media/protected/;
    }
    ...
}
```


### ProtectedFileField and ProtectedImageField

To generate protected files, there are two fields available for the model - [ProtectedFileField][meringue.protected.fields.ProtectedFileField] and [ProtectedImageField][meringue.protected.fields.ProtectedImageField].

```python
class Foo(models.Model):
    file = ProtectedFileField(
        view_name="x_accel_redirect_view",
        host_name="sub",
        disposition="inline",
        nginx_location_getter=_test_getter,
    )
```

* **view_name** - the name of the route handling the file request (mandatory field);
* **host_name** - the host name for reversing to the view, when used in combination with [django-hosts](https://django-hosts.readthedocs.io/en/latest/);
* **disposition** - disposition for the `Content-Disposition` header;
* **nginx_location_getter** - a method that returns the link through which the file will be served by nginx after redirection from the view. The default method is set in the parameter [PROTECTED_NGINX_LOCATION_GETTER][meringue.conf.default_settings.PROTECTED_NGINX_LOCATION_GETTER]. The default method [nginx_location_getter][meringue.protected.utils.nginx_location_getter] returns the original link to the file.

The original properties of the `url` fields have been changed to point to the view specified in the `view_name` attribute.

By default, the field saves the file in the `protected` directory.
