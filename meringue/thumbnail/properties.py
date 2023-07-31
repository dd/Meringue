import re

from meringue.thumbnail.constants import CROP_METHOD_BOTTOM
from meringue.thumbnail.constants import CROP_METHOD_CENTER
from meringue.thumbnail.constants import CROP_METHOD_LEFT
from meringue.thumbnail.constants import CROP_METHOD_RIGTH
from meringue.thumbnail.constants import CROP_METHOD_TOP
from meringue.thumbnail.constants import PROP_BG_COLOR
from meringue.thumbnail.constants import PROP_CROP_METHOD
from meringue.thumbnail.constants import PROP_CURRENT_SIZE
from meringue.thumbnail.constants import PROP_MAX_HEIGHT
from meringue.thumbnail.constants import PROP_MAX_WIDTH
from meringue.thumbnail.constants import PROP_NEW_SIZE
from meringue.thumbnail.constants import PROP_RESIZE_METHOD
from meringue.thumbnail.constants import PROP_RESIZE_STRATEGY
from meringue.thumbnail.constants import RESIZE_METHOD_LIST
from meringue.thumbnail.constants import RESIZE_STRATEGY_LIST
from meringue.thumbnail.exceptions import WrongPropertyOptionError


# cm - crop method
def set_crop_method(value, opt):
    methods = value.split(" ")

    if len(methods) == 1:
        if methods[0] != CROP_METHOD_CENTER:
            msg = "For property `{property}` if it contains one value it can only be `{option}`"
            raise WrongPropertyOptionError(PROP_CROP_METHOD, CROP_METHOD_CENTER, msg)

        methods = [CROP_METHOD_CENTER, CROP_METHOD_CENTER]

    elif len(methods) == 2:  # noqa: PLR2004
        if methods[0] not in [CROP_METHOD_RIGTH, CROP_METHOD_LEFT, CROP_METHOD_CENTER]:
            msg = "Value `{option}` is invalid for property `{property}` at the first position."
            raise WrongPropertyOptionError(PROP_CROP_METHOD, methods[0], msg)

        if methods[1] not in [CROP_METHOD_TOP, CROP_METHOD_BOTTOM, CROP_METHOD_CENTER]:
            msg = "Value `{option}` is invalid for property `{property}` at the second position."
            raise WrongPropertyOptionError(PROP_CROP_METHOD, methods[1], msg)

    else:
        msg = "The property `{property}` must have one or two options."
        raise WrongPropertyOptionError(PROP_CROP_METHOD, None, msg)

    return {PROP_CROP_METHOD: methods}


# rm - resize method
def set_resize_method(method, opt):
    if method not in RESIZE_METHOD_LIST:
        raise WrongPropertyOptionError(PROP_RESIZE_METHOD, method)

    return {PROP_RESIZE_METHOD: method}


# rs - resize strategy
def set_resize_strategy(strategy, opt):
    if strategy not in RESIZE_STRATEGY_LIST:
        raise WrongPropertyOptionError(PROP_RESIZE_STRATEGY, strategy)

    return {PROP_RESIZE_STRATEGY: strategy}


# s - size
def set_size(raw, opt):
    size_re = re.compile(r"(\d+)?x(\d+)?")
    size = [float(i or 0) for i in size_re.search(raw).groups()]

    # расчитываем относительные размеры если один из размеров не указан
    size[0] = (
        size[0] if size[0] else size[1] * opt[PROP_CURRENT_SIZE][0] / opt[PROP_CURRENT_SIZE][1]
    )
    size[1] = (
        size[1] if size[1] else size[0] * opt[PROP_CURRENT_SIZE][1] / opt[PROP_CURRENT_SIZE][0]
    )

    return {PROP_NEW_SIZE: size}


# maxw - max width
def set_max_width(width, opt):
    return {PROP_MAX_WIDTH: float(width)}


# maxh - max height
def set_max_height(height, opt):
    return {PROP_MAX_HEIGHT: float(height)}


# c - background color
def set_bg_color(color, opt):
    tmp = ()

    for i in color.split(" "):
        tmp += (int(i),)

    return {PROP_BG_COLOR: tmp}
