# Configurations

Все настройки для Meringue задаются внутри параметра `MERINGUE` настроек джанго, и а настройках проекта выглядит примерно следующим образом:

```py title="settings.py"
MERINGUE = {
    'UPLOAD_RENAME_HANDLER': 'my_project.upload_handlers.rename_handler',
}
```

Доступ к настройкам библиотеки можно получить следующим образом:

```pycon
>>> from meringue.conf import m_settings
>>> print(m_settings.UPLOAD_RENAME_HANDLER)
my_project.upload_handlers.rename_handler
```

Полный и актуальный список параметров можно посмотреть [тут][meringue.conf.default_settings].
