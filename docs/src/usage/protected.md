# Meringue Protected

This package includes functionality for organizing private files.

The main functionality is encapsulated in [protected_file_view][meringue.protected.views.protected_file_view]. It checks whether the user has access to view the file and serves it.

However, when working with nginx, you can enable the [PROTECTED_SERVE_WITH_NGINX][meringue.conf.default_settings.PROTECTED_SERVE_WITH_NGINX] option. In this case, nginx itself will serve the file instead of Django, using the [internal](https://nginx.org/en/docs/http/ngx_http_core_module.html#internal) directive.


## Usage

In the simplest scenario, you just need to enable view, and everything will work:

```python
urlpatterns = [
    ...
    path(
        "protected/<int:cid>/<slug:field>/<slug:pk>",
        staff_member_required(protected_file_view),
        name="meringue-protected-file",
    ),
    ...
]
```

You can specify any route name, but if you're using the view in conjunction with [ProtectedFileField][meringue.protected.fields.ProtectedFileField] or [ProtectedImageField][meringue.protected.fields.ProtectedImageField], you'll need to specify the corresponding name in the fields as well. This can be useful if you have multiple views for retrieving files.


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


### Extended

To generate protected files, there are two fields available for the model - [ProtectedFileField][meringue.protected.fields.ProtectedFileField] and [ProtectedImageField][meringue.protected.fields.ProtectedImageField].

In these fields, the url attribute is overridden, and it now returns a link to the aforementioned [protected_file_view][meringue.protected.views.protected_file_view].

The field by default saves the file in the directory protected. Additionally, you can specify the name under which you placed the view in your routes using the protected_view_name attribute.
