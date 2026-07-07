from pathlib import Path
from typing import Final
from urllib.parse import urljoin

from django.conf import settings


# CORE #############################################################################################


UPLOAD_RENAME_HANDLER: Final[str] = "meringue.core.upload_handlers.rename_handler"
"""
Path to method for renaming images on upload
"""

COP_YEAR: Final[int | None] = None
"""
Project start year for the copyright tag
"""

COP_YEARS_DIFF: Final[int] = 10
"""
Difference in years for which it is necessary to display the range of years

Specify 1 to display the period for the second year.
"""

CRYPTO_KEY: Final[str] = settings.SECRET_KEY[:32]
"""
Encryption key
"""

FRONTEND_URLS: Final[dict | None] = None
"""
A dict of links to the frontend
"""

FRONTEND_DOMAIN: Final[str | None] = None
"""
Domain for generating absolute links
"""


# API ##############################################################################################


API_ENABLE_ROOT_VIEW: Final[bool] = settings.DEBUG
"""
Option to enable or disable the root view of the [Router][meringue.api.routers.MeringueRouter]
"""


# THUMBNAIL ########################################################################################


THUMBNAIL_GENERATOR_CLASS: Final[str] = "meringue.thumbnail.generators.Thumbnailer"
"""
Thumbnail generator class.
"""

THUMBNAIL_STORAGE_GETTER: Final[str] = "meringue.thumbnail.storage.get_storage"
"""
Dotted path to a method that returns a store.
"""

THUMBNAIL_IMAGE_CLASS: Final[str] = "meringue.thumbnail.images.ThumbnailImage"
"""
Thumbnail image class.
"""

THUMBNAIL_DIR: Final[Path] = Path(settings.MEDIA_ROOT) / Path("m/thumbnail")
"""
Directory for saving thhumbnails.
"""

THUMBNAIL_URL: Final[str] = urljoin(settings.MEDIA_URL, "m/thumbnail")
"""
Url where thumbnails will be available.
"""

THUMBNAIL_PROPERTIES: Final[dict[str, str]] = {
    "cm": "meringue.thumbnail.properties.set_crop_method",
    "rm": "meringue.thumbnail.properties.set_resize_method",
    "rs": "meringue.thumbnail.properties.set_resize_strategy",
    "s": "meringue.thumbnail.properties.set_size",
    "maxw": "meringue.thumbnail.properties.set_max_width",
    "maxh": "meringue.thumbnail.properties.set_max_height",
    "c": "meringue.thumbnail.properties.set_bg_color",
}
"""
Registered thumbnail properties.
"""

THUMBNAIL_ACTIONS: Final[dict[str, str]] = {
    "crop": "meringue.thumbnail.actions.crop",
    "resize": "meringue.thumbnail.actions.resize",
}
"""
Registered thumbnail actions.
"""

THUMBNAIL_DEFAULT_CROP_METHOD: Final[list[str]] = ["center", "center"]
"""
Default crop method.
"""

THUMBNAIL_DEFAULT_RESIZE_METHOD: Final[str] = "contain"
"""
Default resize method.
"""

THUMBNAIL_DEFAULT_RESIZE_STRATEGY: Final[str] = "standard"
"""
Default resize strategy.
"""

THUMBNAIL_DEFAULT_BG_COLOR: Final[tuple[int]] = (200, 200, 200, 0)
"""
Default background color for crop in RGBA format.
"""


THUMBNAIL_SAVE_PARAMS_BY_FORMAT: Final[dict[str, dict]] = {
    "GIF": {"optimize": True},
    "JPEG": {"quality": 85, "optimize": True},
    "PNG": {"optimize": True, "compress_level": 5},
    "TIFF": {"quality": 85},
    "WEBP": {"quality": 85},
}
"""
List of default options for saving thumbnails images by format.
"""

THUMBNAIL_IMAGE_OPTIMIZE_HANDLER: Final[str | None] = "meringue.thumbnail.optimizers.optimize"
"""
Dotted path to a function that optimizes thumbnail image before saving it to storage.
The function receives a [ThumbnailImage][meringue.thumbnail.images.ThumbnailImage] instance and
an in-memory image file and must return an in-memory image file.
"""

THUMBNAIL_OPTIMIZERS: Final[dict[str, dict]] = {}
"""
Built-in thumbnail optimizer settings.

Keys are optimizer names, values are optimizer-specific settings.
Empty dictionary disables built-in optimizers.

For `oxipng`, set `binary` to the oxipng executable path or command name.
The default command-line options can be overridden with the `options` value,
as either a string or a list of strings.

Example:
    ```python
    {
        "oxipng": {
            "binary": "oxipng",
            "options": "-o 4 --strip all",
        },
    }
    ```
"""

THUMBNAIL_DUMMYIMAGE_TEMPLATE: Final[str] = "//dummyimage.com/{width}x{height}/9e9e9e/424242.png"
"""
Template for dummy image URL. Supports `{width}` and `{height}` placeholders.
"""

THUMBNAIL_DEFAULT_FORMAT: Final[str] = "PNG"
"""
Default thumbnail image format.
"""


# PROTECTED ########################################################################################


PROTECTED_SERVE_WITH_NGINX: Final[bool] = not settings.DEBUG
"""
The option implies the distribution of protected files by nginx. Instead of serving the file in
response.

The view [x_accel_redirect_view][meringue.protected.views.x_accel_redirect_view] adds the
X-Accel-Redirect header with a link to the file.
"""

PROTECTED_NGINX_LOCATION_GETTER: Final[str] = "meringue.protected.utils.nginx_location_getter"
"""
Default getter for the link to the file where nginx should serve it after access verification.
"""
