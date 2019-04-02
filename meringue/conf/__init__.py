# -*- coding: utf-8 -*-

from django.conf import settings as _settings

from meringue.conf import default_settings


class Settings:

    def __init__(self, default=default_settings):

        for setting in default.__all__:
            if not setting.isupper():
                continue

            default_value = getattr(default, setting)
            setting_value = getattr(_settings, f'MERINGUE_{setting}', default_value)
            setattr(self, setting, setting_value)


settings = Settings()
