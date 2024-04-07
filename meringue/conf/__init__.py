import warnings
from types import ModuleType
from typing import Any
from typing import Final

from django.conf import settings
from django.core.signals import setting_changed
from django.dispatch import receiver
from django.utils.module_loading import import_string

from meringue.conf import default_settings


SETTING_KEY: Final[str] = "MERINGUE"
"""
Parameter name in django settings for meringue settings.

Examples:
    ```py title="settings.py"
    MERINGUE = {
        "FRONTEND_URL": "http://meringue.local:9000/",
    }
    ```
"""


DEPRECATED_PARAMS: Final[dict[str, str]] = {}
"""
Dict with deprecated options and warning texts for them.

Examples:
    ```py
    DEPRECATED_PARAMS = {
        "PROTOCOL": "The `PROTOCOL` option is deprecated, use `BACKEND_PROTOCOL` instead.",
    }
    ```
"""

PARAMS_TO_IMPORT: Final[list[str]] = [
    "UPLOAD_RENAME_HANDLER",
    "THUMBNAIL_GENERATOR_CLASS",
    "THUMBNAIL_STORAGE_GETTER",
    "THUMBNAIL_IMAGE_CLASS",
    "THUMBNAIL_PROPERTIES",
    "THUMBNAIL_ACTIONS",
    "PROTECTED_NGINX_LOCATION_GETTER",
]
"""
List of options that contain the path to the module and must be imported.

Examples:
    ```py
    PARAMS_TO_IMPORT = [
        "UPLOAD_RENAME_HANDLER",
    ]
    ```
"""


def import_list(path_list: list[str]) -> list[Any]:
    """
    Import a list of dotted modules.

    Attributes:
        path_list: List of dotted paths.

    Raises:
        TypeError: Wrong dotted path data type for import.
        ImportError: Import error.

    Returns:
        List of imported attributes/classes.
    """

    result = []

    for dotted_path in path_list:
        if not isinstance(dotted_path, str):
            msg = f"`{type(dotted_path).__name__}` data type is not supported for import."
            raise TypeError(msg, dotted_path)

        try:
            result.append(import_string(dotted_path))
        except ImportError as err:
            msg = f"`{dotted_path}` import error."
            raise ImportError(msg, path=dotted_path) from err

    return result


def import_dict(path_dict: dict[str, str]) -> dict[str, Any]:
    """
    Import a dictionary with dotted path as key value.

    Attributes:
        path_dict: Dictionary with dotted path as key value.

    Raises:
        TypeError: Wrong dotted path data type for import.
        ImportError: Import error.

    Returns:
        Dict with imported attributes/classes as key value.
    """

    result = {}

    for key, dotted_path in path_dict.items():
        if not isinstance(dotted_path, str):
            msg = f"`{type(dotted_path).__name__}` data type is not supported for import."
            raise TypeError(msg, dotted_path)

        try:
            result[key] = import_string(dotted_path)
        except ImportError as err:
            msg = f"`{dotted_path}` import error."
            raise ImportError(msg, path=dotted_path) from err

    return result


def import_parameter(value: str | list[str] | dict[str, str]) -> Any | list[Any] | dict[str, Any]:
    """
    Method for importing modules in settings parameter.

    Attributes:
        value: Settings parameter value to import.

    Returns:
        Imported parameter.
    """

    if isinstance(value, str):
        try:
            return import_string(value)
        except ImportError as err:
            msg = f"`{value}` import error."
            raise ImportError(msg, path=value) from err

    if isinstance(value, list):
        return import_list(value)

    if isinstance(value, dict):
        return import_dict(value)

    msg = f"`{type(value).__name__}` data type is not supported for import."
    raise TypeError(msg, value)


class Settings:
    """
    A settings object.

    The settings are obtained from the django settings by the name of the key which should contain
    an object with all the application settings.
    """

    def __init__(
        self,
        setting_key: str,
        defaults: dict[str, str],
        deprecated_params: dict[str, str] | None = None,
        params_to_impoprt: list[str] | None = None,
    ):
        """
        Attributes:
            setting_key: Settings key in django settings list.
            defaults: Dict with default parameter values. Used as a list of available settings.
            deprecated_params: Dict with deprecated options and warning texts for them.
            params_to_impoprt: List of options that contain the path to the module and must be
                imported.
        """

        self.setting_key = setting_key
        if isinstance(defaults, ModuleType):
            self.defaults = {}
            for key in dir(defaults):
                if key.isupper():
                    self.defaults[key] = getattr(defaults, key)
        else:
            self.defaults = defaults
        self.deprecated_params = deprecated_params or {}
        self.params_to_impoprt = params_to_impoprt or []
        self._cached_attrs = set()
        self.reset()

    def __getattr__(self, attr: str) -> Any:
        """
        Gets the parameter value and caches it in the attributes of the settings object.

        Attributes:
            attr: Setting parameter name.

        Raises:
            AttributeError: Error when trying to get an unregistered parameter.

        Warns:
            DeprecationWarning: A warning that the parameter is deprecated.

        Returns:
            Setting value.
        """

        if attr not in self.defaults:
            raise AttributeError("Invalid setting key: '%s'" % attr)

        if attr in self.deprecated_params:
            warnings.warn(self.deprecated_params[attr], DeprecationWarning, stacklevel=2)

        val = self.user_params.get(attr, self.defaults[attr])

        if attr in self.params_to_impoprt:
            try:
                val = import_parameter(val)

            except ImportError as err:
                msg = f"Error importing `{err.path}` attribute/class in `{attr}` parameter."
                raise ImportError(msg) from err

            except TypeError as err:
                msg = (
                    f"The `{err.args[1]}` value of the `{attr}` parameter is not available for "
                    "import."
                )
                raise TypeError(msg) from None

        self._cached_attrs.add(attr)
        setattr(self, attr, val)
        return val

    def reset(self):
        """
        Reset downloaded settings, as well as clearing the cache.
        """

        for attr in self._cached_attrs:
            delattr(self, attr)
        self._cached_attrs = set()
        self.user_params = getattr(settings, self.setting_key, {})


m_settings = Settings(SETTING_KEY, default_settings, DEPRECATED_PARAMS, PARAMS_TO_IMPORT)


@receiver(setting_changed)
def reset_settings(*args, **kwargs):
    """
    Settings change signal handler.
    """

    if kwargs["setting"] == SETTING_KEY:
        m_settings.reset()
