# -*- coding: utf-8 -*-

from django.template import Library

from wo_nucleum.utils.thumbnails import get_thumbnail


register = Library()


@register.filter
def thumbnail(filename, args=''):
    '''
    Аргументы фильтра:
        crop - изменения размера холста
        resize - изменение размера изображения
        s:<width>x<height> - размер изображения
        q:<quality> - качество конечного изображения 0-100
        c:<color> - цвет заливки для кропа в формате rgba
            (c:255 255 255 255)
        rm:scale|inscribe|stretch - метод ресайза вписать в размер или
            растянуть
        cm:left|center|rigth top|center|bottom - точка отсчёта для кропа

    TO-DO:
        watermark
        подгон размеров

    '''

    task_list = args.split(',')
    return get_thumbnail(filename=filename, task_list=task_list)
