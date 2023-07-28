# Meringue core

This is a basic package that contains a variety of general purpose functionality such as abstract models, various handlers, utilities, and more.


## Mixins

### CMTimeMixin

A primitive abstract model that adds the _ctime_ and _mtime_ fields to your model.


### SortingMixin

An abstract model that adds a sortable field, as well as a manager with sorting correction functionality.


#### correction_sorting

::: meringue.core.query.SortingQuerySet.correction_sorting
	options:
		show_root_heading: false
		show_root_toc_entry: false
		show_source: false


### PublicationMixin

::: meringue.core.models.PublicationMixin
	options:
		show_root_heading: false
		show_root_toc_entry: false
		show_source: false
		show_bases: false


#### published

::: meringue.core.query.PublicationQuerySet.published
	options:
		show_root_heading: false
		show_root_toc_entry: false
		show_source: false


#### unpublished

::: meringue.core.query.PublicationQuerySet.unpublished
	options:
		show_root_heading: false
		show_root_toc_entry: false
		show_source: false


### PublicationDatesMixin

::: meringue.core.models.PublicationDatesMixin
	options:
		show_root_heading: false
		show_root_toc_entry: false
		show_source: false
		show_bases: false


#### published

::: meringue.core.query.PublicationQuerySet.published
	options:
		show_root_heading: false
		show_root_toc_entry: false
		show_source: false


#### unpublished

::: meringue.core.query.PublicationQuerySet.unpublished
	options:
		show_root_heading: false
		show_root_toc_entry: false
		show_source: false


## Utils


### datetime

#### format_date_from_to

::: meringue.core.utils.datetime.format_date_from_to
	options:
		show_root_heading: false
		show_root_toc_entry: false
		show_source: false


### crypt

This module contains two extremely simplified functions for encrypting and decrypting a message using the AES algorithm and the GCM method. The main task that these functions are designed to solve is to encrypt small amounts of data for situations such as password recovery links and the like.

!!! note
	These functions are just a wrapper for encryption methods from the [pycryptodome](https://www.pycryptodome.org/) library (you also need to install it).


#### encrypt_message

::: meringue.core.utils.crypt.encrypt_message
	options:
		show_root_heading: false
		show_root_toc_entry: false
		show_source: false
		show_docstring_raises: false
		show_docstring_returns: false
		show_docstring_attributes: false

#### decrypt_message

::: meringue.core.utils.crypt.decrypt_message
	options:
		show_root_heading: false
		show_root_toc_entry: false
		show_source: false
		show_docstring_raises: false
		show_docstring_returns: false
		show_docstring_attributes: false

Methods for encryption use a key that can be set in the [CRYPTO_KEY][meringue.conf.default_settings.CRYPTO_KEY] parameter. By default, the parameter uses the first 32 characters of [SECRET_KEY](https://docs.djangoproject.com/en/4.2/ref/settings/#std-setting-SECRET_KEY).


### frontend

#### get_link

[get_link][meringue.core.utils.frontend.get_link] is a method for getting a link to a resource.

Modern sites mainly work according to the scheme when the backend provides an api to which the front sends requests, in this regard, [reverse](https://docs.djangoproject.com/en/4.2/ref/urlresolvers/#reverse), which provides django, cannot give actual links to the resource, but links are still needed in the backend (for example, in letters and sms sent to the user or in admin panel for managers). As a result, this small utility was implemented that will help you get a link to the desired resource.

To use the utility, you must specify a list of links in the [FRONTEND_URLS][meringue.conf.default_settings.FRONTEND_URLS] parameter, and also, if you plan to receive absolute links, the frontend domain in the [FRONTEND_DOMAIN][meringue.conf.default_settings.FRONTEND_DOMAIN] parameter:

```py title="settings.py"
MERINGUE = {
    "FRONTEND_URLS": {
        "index": "/"
        "user": "/user/{id}"
    },
    "FRONTEND_DOMAIN": "https://example.com",
}
```

You can get links in code like this:

```pycon
>>> from meringue.core.utils.frontend import get_link
>>> get_link("index")
https://example.com/

>>> get_link("user", id=123)
https://example.com/user/123
```


## Templatetags


### cop_year

::: meringue.core.templatetags.meringue_base.cop_year
	options:
		show_root_heading: false
		show_root_toc_entry: false
		show_source: false

For the tag to work, you must fill in the [COP_YEAR][meringue.conf.default_settings.COP_YEAR] parameter in the settings.

Also, in the [COP_YEARS_DIFF][meringue.conf.default_settings.COP_YEARS_DIFF] parameter, you can specify the minimum difference in years when the period in copyrights will be displayed, and not the current year.


### date_range

::: meringue.core.templatetags.meringue_base.date_range
	options:
		show_root_heading: false
		show_root_toc_entry: false
		show_source: false


## Translations

If you use [djano-modeltranslation](https://django-modeltranslation.readthedocs.io/en/latest/), then when connecting `meringue.core`, you can register fields for translations by setting the list of fields in the `m_translate_fields` field in the meta of the corresponding model:

```py
class FooModel(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        m_translate_fields = ["name", ]
```


## Upload handlers

The standard django load handlers leave the original file name where possible. However, often when uploading a file to the server, the file can be called somehow ugly (and sometimes indecent), in order to avoid this problem, the following two upload handlers are implemented - [MemoryFileUploadHandler][meringue.core.upload_handlers.MemoryFileUploadHandler] and [TemporaryFileUploadHandler][meringue.core.upload_handlers.TemporaryFileUploadHandler]. These two loaders replace the corresponding django loaders but in the process they rename the file being loaded.

The renaming process can be overridden by specifying your own renaming method in the [UPLOAD_RENAME_HANDLER][meringue.conf.default_settings.UPLOAD_RENAME_HANDLER] parameter.

To use them, specify them in the [FILE_UPLOAD_HANDLERS](https://docs.djangoproject.com/en/4.2/ref/settings/#std-setting-FILE_UPLOAD_HANDLERS) parameter:

```python
FILE_UPLOAD_HANDLERS = [
    "meringue.core.upload_handlers.TemporaryFileUploadHandler",
    "meringue.core.upload_handlers.MemoryFileUploadHandler",
]
```


## Views


### im_a_teapot

::: meringue.core.views.im_a_teapot
	options:
		show_root_heading: false
		show_root_toc_entry: false
		show_source: false
