from typing import Final


# Properties keys
PROP_BG_COLOR: Final[str] = "bg_color"
PROP_CROP_METHOD: Final[str] = "crop_method"
PROP_CURRENT_SIZE: Final[str] = "current_size"
PROP_MAX_HEIGHT: Final[str] = "max_height"
PROP_MAX_WIDTH: Final[str] = "max_width"
PROP_NEW_SIZE: Final[str] = "new_size"
PROP_RESIZE_METHOD: Final[str] = "resize_method"
PROP_RESIZE_STRATEGY: Final[str] = "resize_strategy"


# Crop methods
CROP_METHOD_CENTER: Final[str] = "center"
CROP_METHOD_TOP: Final[str] = "top"
CROP_METHOD_RIGTH: Final[str] = "rigth"
CROP_METHOD_BOTTOM: Final[str] = "bottom"
CROP_METHOD_LEFT: Final[str] = "left"
CROP_METHOD_LIST: Final[list[str]] = [
    CROP_METHOD_CENTER,
    CROP_METHOD_TOP,
    CROP_METHOD_RIGTH,
    CROP_METHOD_BOTTOM,
    CROP_METHOD_LEFT,
]

# Resize methods
RESIZE_METHOD_COVER: Final[str] = "cover"
RESIZE_METHOD_CONTAIN: Final[str] = "contain"
RESIZE_METHOD_STRETCH: Final[str] = "stretch"
RESIZE_METHOD_LIST: Final[list[str]] = [
    RESIZE_METHOD_COVER,
    RESIZE_METHOD_CONTAIN,
    RESIZE_METHOD_STRETCH,
]

# Resize strategy
RESIZE_STRATEGY_DO_NOT_INCREASE_SIZE: Final[str] = "no_increase"
RESIZE_STRATEGY_STANDART: Final[str] = "standart"
RESIZE_STRATEGY_DO_NOT_REDUCE_SIZE: Final[str] = "no_reduce"
RESIZE_STRATEGY_LIST: Final[list[str]] = [
    RESIZE_STRATEGY_DO_NOT_INCREASE_SIZE,
    RESIZE_STRATEGY_STANDART,
    RESIZE_STRATEGY_DO_NOT_REDUCE_SIZE,
]

# Formats
FORMAT_BMP: Final[str] = "BMP"
"""Format BMP"""
FORMAT_EPS: Final[str] = "EPS"
"""Format EPS"""
FORMAT_GIF: Final[str] = "GIF"
"""Format GIF"""
FORMAT_ICO: Final[str] = "ICO"
"""Format ICO"""
FORMAT_JPEG: Final[str] = "JPEG"
"""Format JPEG"""
FORMAT_PNG: Final[str] = "PNG"
"""Format PNG"""
FORMAT_TIFF: Final[str] = "TIFF"
"""Format TIFF"""
FORMAT_WEBP: Final[str] = "WEBP"
"""Format WEBP"""

# Extension
EXTENSION_BMP: Final[str] = ".bmp"
"""Extension .bmp"""
EXTENSION_EPS: Final[str] = ".eps"
"""Extension .eps"""
EXTENSION_GIF: Final[str] = ".gif"
"""Extension .gif"""
EXTENSION_ICO: Final[str] = ".ico"
"""Extension .ico"""
EXTENSION_JPG: Final[str] = ".jpg"
"""Extension .jpg"""
EXTENSION_JPEG: Final[str] = ".jpeg"
"""Extension .jpeg"""
EXTENSION_JFIF: Final[str] = ".jfif"
"""Extension .jfif"""
EXTENSION_PNG: Final[str] = ".png"
"""Extension .png"""
EXTENSION_TIFF: Final[str] = ".tiff"
"""Extension .tiff"""
EXTENSION_WEBP: Final[str] = ".webp"
"""Extension .webp"""


FORMATS_BY_EXTENSIONS: Final[dict[str, str]] = {
    EXTENSION_BMP: FORMAT_BMP,
    EXTENSION_EPS: FORMAT_EPS,
    EXTENSION_GIF: FORMAT_GIF,
    EXTENSION_ICO: FORMAT_ICO,
    EXTENSION_JPG: FORMAT_JPEG,
    EXTENSION_JPEG: FORMAT_JPEG,
    EXTENSION_JFIF: FORMAT_JPEG,
    EXTENSION_PNG: FORMAT_PNG,
    EXTENSION_TIFF: FORMAT_TIFF,
    EXTENSION_WEBP: FORMAT_WEBP,
}
"""Formats by extensions"""


EXTENSIONS_BY_FORMATS: Final[dict[str, str]] = {
    # DIB
    # BUFR
    # PCX
    # FITS
    # GRIB
    # HDF5
    # JPEG2000
    # IM
    # MPO
    # MSP
    # PALM
    # PDF
    # PPM
    # SGI
    # SPIDER
    # TGA
    # WMF
    # XBM
    FORMAT_BMP: EXTENSION_BMP,
    FORMAT_EPS: EXTENSION_EPS,
    FORMAT_GIF: EXTENSION_GIF,
    FORMAT_ICO: EXTENSION_ICO,
    FORMAT_JPEG: EXTENSION_JPG,
    FORMAT_PNG: EXTENSION_PNG,
    FORMAT_TIFF: EXTENSION_TIFF,
    FORMAT_WEBP: EXTENSION_WEBP,
}
"""Extensions by formats"""

FORMATS_WITH_ALPHA_SUPPORT: Final[list[str]] = [
    FORMAT_BMP,
    FORMAT_EPS,
    FORMAT_GIF,
    FORMAT_ICO,
    FORMAT_PNG,
    FORMAT_TIFF,
    FORMAT_WEBP,
]
"""Formats with alpha support"""
