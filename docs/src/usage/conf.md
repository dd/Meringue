# Configurations

All settings for Meringue are set inside the `MERINGUE` parameter of the django settings, and in the project settings it looks something like this:

```py title="settings.py"
MERINGUE = {
    'UPLOAD_RENAME_HANDLER': 'my_project.upload_handlers.rename_handler',
}
```

Library settings can be accessed as follows:

```pycon
>>> from meringue.conf import m_settings
>>> print(m_settings.UPLOAD_RENAME_HANDLER)
my_project.upload_handlers.rename_handler
```

A complete and up-to-date list of parameters can be found [here][meringue.conf.default_settings].
