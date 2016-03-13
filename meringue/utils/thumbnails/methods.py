# -*- coding: utf-8 -*-

import logging  # noqa
import math

from PIL import Image


def get_size(options, max_sizes=True):
    new_size = options['new_size']
    if max_sizes:
        if options['max_width'] and new_size[0] > options['max_width']:
            new_size[0] = options['max_width']
        if options['max_height'] and new_size[1] > options['max_height']:
            new_size[1] = options['max_height']
    return new_size


def crop(image, options):
    new_size = get_size(options)
    new_size = [int(new_size[0]), int(new_size[1])]

    current_size = options['current_size']
    thumb = Image.new(mode='RGBA', size=new_size, color=options['bg_color'])

    # позиционируем новое изображение
    if options['crop_method'][0] == 'left':
        x = 0
    elif options['crop_method'][0] == 'right':
        x = new_size[0] - current_size[0]
    else:
        x = (new_size[0] - current_size[0]) / 2

    if options['crop_method'][1] == 'left':
        y = 0
    elif options['crop_method'][1] == 'right':
        y = new_size[1] - current_size[1]
    else:
        y = (new_size[1] - current_size[1]) / 2

    thumb.paste(image, (int(x), int(y)))
    image = thumb
    options['current_size'] = new_size

    return image


def resize(image, options):
    new_size = get_size(options)
    current_size = options['current_size']

    if options['resize_method'] in ['cover', 'contain']:

        # заполнить всё новое изображение
        if options['resize_method'] == 'cover':
            res = max(new_size[0] / current_size[0],
                      new_size[1] / current_size[1])

        # вписать изображение полностью
        elif options['resize_method'] == 'contain':
            res = min(new_size[0] / current_size[0],
                      new_size[1] / current_size[1])

        new_size = [math.floor(current_size[0] * res),
                    math.floor(current_size[1] * res)]

        # при сжатии никак не меняем конечный размер

    new_size = [int(i) for i in new_size]
    image = image.resize(new_size, resample=Image.ANTIALIAS)
    options['current_size'] = new_size

    return image


method_list = {
    'crop': crop,
    'resize': resize,
}
