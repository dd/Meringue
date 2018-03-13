# -*- coding: utf-8 -*-

import logging  # noqa
import re


# cm
def set_crop_method(method, opt):
    return {'crop_method': method.split(' ')}


# rm
def set_resize_method(method, opt):
    return {'resize_method': method}


# s
def set_size(raw, opt):
    size_re = re.compile(r'(\d+)x(\d+)')
    size = [float(i) for i in size_re.search(raw).groups()]

    # расчитываем относительные размеры если один из размеров не указан
    size[0] = size[0] if size[0] else size[1] * opt['current_size'][0] / \
        opt['current_size'][1]
    size[1] = size[1] if size[1] else size[0] * opt['current_size'][1] / \
        opt['current_size'][0]

    return {'new_size': size}


# maxw
def set_max_width(width, opt):
    return {'max_width': float(width)}


# maxh
def set_max_height(height, opt):
    return {'max_height': float(height)}


# q
def set_quality(quality, opt):
    return {'quality': int(quality)}


# c
def set_bg_color(color, opt):
    tmp = tuple()
    for i in color.split(' '):
        tmp += (int(i), )
    return {'bg_color': tmp}


property_list = {
    'cm': set_crop_method,
    'rm': set_resize_method,
    's': set_size,
    'maxw': set_max_width,
    'maxh': set_max_height,
    'q': set_quality,
    'c': set_bg_color,
}
