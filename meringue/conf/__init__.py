import warnings
from typing import Any
from typing import Final

from django.conf import settings as dj_settings
from django.utils.module_loading import import_string

from meringue.conf import default_settings


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

PARAMS_TO_IMPORT: Final[list[str]] = []
"""
List of options that contain the path to the module and must be imported.

Examples:
    ```py
    PARAMS_TO_IMPORT = [
        "UPLOAD_RENAME_HANDLER",
    ]
    ```
"""


def import_from_string(val: str, attr: str) -> Any:
    """
    Imports a dotted module path and returns the attribute/class.

    Attributes:
        val: Dotted path to imported module.
        attr: The name of the parameter in the library settings.

    Raises:
        ImportError: Attribute/class not exists.

    Returns:
        Imported attribute/class.
    """

    try:
        return import_string(val)
    except ImportError as e:
        msg = "Could not import '%s' for API setting '%s'. %s: %s." % (
            val,
            attr,
            e.__class__.__name__,
            e,
        )
        raise ImportError(msg)


class Settings:
    def __init__(
        self,
        defaults: dict[str, str],
        deprecated_params: dict[str, str],
        params_to_impoprt: list[str],
    ):
        """
        Attributes:
            defaults: Dict with default options values.
            deprecated_params: Dict with deprecated options and warning texts for them.
            params_to_impoprt: List of options that contain the path to the module and must be imported.
        """
        self.defaults = defaults
        self.deprecated_params = deprecated_params
        self.params_to_impoprt = params_to_impoprt

    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError("Invalid API setting: '%s'" % attr)

        if attr in self.deprecated_params:
            warnings.warn(self.deprecated_params[attr], DeprecationWarning)

        if attr in self.params_to_impoprt:
            val = import_from_string(val, attr)

        setattr(self, attr, val)
        return val


settings = Settings(default_settings, DEPRECATED_PARAMS, PARAMS_TO_IMPORT)
