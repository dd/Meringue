from typing import Final

import django
from django.conf import settings
from django.core.files.storage import Storage

from meringue.conf import m_settings


def get_storage() -> Storage:
    """
    Finds the default storage class and returns its instance for use with thumbnails.

    !!! warning
        This method has not been tested with custom stores and complex parameter sets.

    Returns:
        Storage instance.
    """

    if django.VERSION < (4, 2):
        DefaultStorage = settings.DEFAULT_FILE_STORAGE  # noqa: N806
        storage = DefaultStorage(
            location=m_settings.THUMBNAIL_DIR,
            base_url=m_settings.THUMBNAIL_URL,
        )
    else:
        from django.conf import DEFAULT_STORAGE_ALIAS
        from django.core.files.storage import storages

        params = storages.backends[DEFAULT_STORAGE_ALIAS]
        params["location"] = m_settings.THUMBNAIL_DIR
        params["base_url"] = m_settings.THUMBNAIL_URL
        storage = storages.create_storage(params)

    return storage


default_storage: Final[Storage] = m_settings.THUMBNAIL_STORAGE_GETTER()
