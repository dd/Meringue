import math

from PIL import Image

from meringue.thumbnail import constants
from meringue.thumbnail.exceptions import ActionError


def get_size(options, max_sizes=True):
    """
    Calc image size
    """

    new_size = options[constants.PROP_NEW_SIZE]
    if max_sizes:
        if options[constants.PROP_MAX_WIDTH] and new_size[0] > options[constants.PROP_MAX_WIDTH]:
            new_size[0] = options[constants.PROP_MAX_WIDTH]

        if options[constants.PROP_MAX_HEIGHT] and new_size[1] > options[constants.PROP_MAX_HEIGHT]:
            new_size[1] = options[constants.PROP_MAX_HEIGHT]

    return new_size


def crop(image, options):
    """
    Crop image
    """

    new_size = get_size(options)
    new_size = [int(new_size[0]), int(new_size[1])]

    current_size = options[constants.PROP_CURRENT_SIZE]
    thumb = Image.new(mode="RGBA", size=new_size, color=options[constants.PROP_BG_COLOR])

    # позиционируем новое изображение по X
    if options[constants.PROP_CROP_METHOD][0] == constants.CROP_METHOD_LEFT:
        x = 0
    elif options[constants.PROP_CROP_METHOD][0] == constants.CROP_METHOD_RIGTH:
        x = new_size[0] - current_size[0]
    else:
        # CROP_METHOD_CENTER
        x = (new_size[0] - current_size[0]) / 2

    # позиционируем новое изображение по Y
    if options[constants.PROP_CROP_METHOD][1] == constants.CROP_METHOD_TOP:
        y = 0
    elif options[constants.PROP_CROP_METHOD][1] == constants.CROP_METHOD_BOTTOM:
        y = new_size[1] - current_size[1]
    else:
        # CROP_METHOD_CENTER
        y = (new_size[1] - current_size[1]) / 2

    thumb.paste(image, (int(x), int(y)))
    image = thumb
    options[constants.PROP_CURRENT_SIZE] = new_size

    return image


def resize(image, options):
    """
    Resize image
    """

    new_size = get_size(options)
    current_size = options[constants.PROP_CURRENT_SIZE]
    method = options[constants.PROP_RESIZE_METHOD]
    strategy = options[constants.PROP_RESIZE_STRATEGY]

    if method in [constants.RESIZE_METHOD_COVER, constants.RESIZE_METHOD_CONTAIN]:
        # режим cover - заполнить всё новое изображение старым
        if method == constants.RESIZE_METHOD_COVER:
            res = max(
                new_size[0] / current_size[0],
                new_size[1] / current_size[1],
            )

        # режим contain - вписать изображение полностью в новый размер
        elif method == constants.RESIZE_METHOD_CONTAIN:
            res = min(
                new_size[0] / current_size[0],
                new_size[1] / current_size[1],
            )

        if strategy == constants.RESIZE_STRATEGY_DO_NOT_INCREASE_SIZE and res > 1:
            # отказываем в увеличении размера
            new_size = current_size.copy()

        elif strategy == constants.RESIZE_STRATEGY_DO_NOT_REDUCE_SIZE and res < 1:
            # отказываем в уменьшении размера
            new_size = current_size.copy()

        else:
            new_size = [math.floor(current_size[0] * res), math.floor(current_size[1] * res)]

    else:  # noqa: PLR5501
        # RESIZE_METHOD_STRETCH
        # при сжатии никак не меняем конечный размер

        if strategy != constants.RESIZE_STRATEGY_STANDART:
            msg = (
                f"The `{constants.RESIZE_METHOD_STRETCH}` method is not compatible "
                f"with the `{strategy}` strategy."
            )
            raise ActionError(msg)

    new_size = [int(new_size[0]), int(new_size[1])]

    if new_size[0] != current_size[0] or new_size[1] != current_size[1]:
        image = image.resize(new_size, resample=Image.LANCZOS)
        options[constants.PROP_CURRENT_SIZE] = new_size

    return image
