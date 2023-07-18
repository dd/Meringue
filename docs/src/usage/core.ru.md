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


### format_date_from_to

::: meringue.core.utils.datetime.format_date_from_to
	options:
		show_root_heading: false
		show_root_toc_entry: false
		show_source: false


### crypt

Этот модуль содержит две максимально упращённые функции для шифрования и дешифрования сообщения с помощью алгоритма AES и метода GCM. Основная задача которую призваны решить эти функции это шифрование небольших объёмов данных для таких ситуаций как ссылки на восстановленние пароля и аналогичное.

!!! note
	Эти функции лишь обёртка для методов шифрования из библиотеки [pycryptodome](https://www.pycryptodome.org/) (её так же необходимо поставить).


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

### frontend

<a name="get_link"></a>
<!-- #### get_link -->

[get_link][meringue.core.utils.frontend.get_link] это метод для получени ссылки на фронтенд.

Современные сайты в основном работают по схеме когда бекенд предоставляет апи к которому фронт отправляет запросы, в связи с этим [reverse](https://docs.djangoproject.com/en/4.2/ref/urlresolvers/#reverse) который предоставляет джанго не может дать актуальные ссылки на ресурс, однако ссылки всё ещё нужны в бекенде (например в письмах и смс отправляемых пользователю или в админке для менедеров). В результате была реализована эта небольшая утилита которая поможет получить ссылку на нужный ресурс.

Чтобы использовать утилиту необходимо указать список ссылок в настройках проекта, а так же если планируется получать абсолютные ссылки домен фронтенда:

```pycon title="settings.py"
MERINGUE={
    "FRONTEND_URLS": {
        "index": "/"
        "user": "/user/{id}"
    },
    "FRONTEND_DOMAIN": "https://example.com",
}
```

Получить ссылки в коде можно следующим образом:

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


### date_range

::: meringue.core.templatetags.meringue_base.date_range
	options:
		show_root_heading: false
		show_root_toc_entry: false
		show_source: false


## Translations

Если вы используете [djano-modeltranslation](https://django-modeltranslation.readthedocs.io/en/latest/), то при подключеннии `meringue.core` регистрировать поля для переводов можно заданием списка полей в поле `m_translate_fields` в мета соответствующей модели:

```py
class FooModel(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        m_translate_fields = ["name", ]
```


## Views


### im_a_teapot

::: meringue.core.views.im_a_teapot
	options:
		show_root_heading: false
		show_root_toc_entry: false
		show_source: false
