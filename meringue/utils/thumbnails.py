# -*- coding: utf-8 -*-

from PIL import Image
import logging
import math
import os.path
import re
try:
    from hashlib import md5
except ImportError:
    from md5 import md5

from django.conf import settings

from meringue import settings as wn_settings


class Thumbnail(object):

    crop_method = wn_settings.THUMBNAIL_CROP_MOTHOD
    resize_method = wn_settings.THUMBNAIL_RESIZE_MOTHOD
    quality = wn_settings.THUMBNAIL_QUALITY
    color = wn_settings.THUMBNAIL_COLOR

    store_dir = wn_settings.THUMBNAIL_DIR
    store_url = wn_settings.THUMBNAIL_URL

    def __init__(self, filename, proc='extra@1'):
        if os.path.isabs(filename):
            self.filename = filename
        else:
            self.filename = os.path.join(settings.MEDIA_ROOT, filename)

        if not os.path.isfile(os.path.realpath(self.filename)):
            raise Exception('File \'%s\' does not exist.' % filename)
        self.proc = proc
        if not self.is_valid_thumbnail():
            self.make_thumbnail()

    def is_valid_thumbnail(self):
        '''
            проверяет существование и актуальность превью.
        '''
        if os.path.isfile(self.thumbnail_filename):
            return os.path.getmtime(self.filename) < os.path.getmtime(
                self.thumbnail_filename
            )
        return False

    def get_thumbnail_filename(self):
        if getattr(self, '_thumbnail_filename', None) is None:
            filename = '%s.png' % (self.get_hash(), )
            if not os.path.exists(self.store_dir):
                os.mkdir(self.store_dir)
            self._thumbnail_filename = os.path.join(self.store_dir, filename)
        return self._thumbnail_filename
    thumbnail_filename = property(get_thumbnail_filename)

    def get_hash(self):
        '''
            Указывать конечный размер?? зачем?
        '''
        hash = [i for i in self.proc]  # self.proc
        hash.append(os.path.basename(self.filename))
        return md5(unicode(hash)).hexdigest()

    def make_thumbnail(self):
        try:
            self.image = Image.open(self.filename)
            self.image = self.image.convert('RGBA')
        except IOError, detail:
            raise Exception(detail)

        self.size = [float(i) for i in self.image.size]
        for proc in self.proc:
            try:
                change = getattr(self, '_%s' % proc)
                change()
            except AttributeError:
                method, args = proc.split(':')
                change = getattr(self, '_%s' % method)
                change(args)

        self.image.save(self.thumbnail_filename, 'PNG',
                        quality=self.quality, optimize=1)

    # методы
    def _crop(self):
        thumb = Image.new(mode='RGBA', size=self.new_size, color=self.color)

        if self.crop_method[0] == 'left':
            x = 0
        elif self.crop_method[0] == 'right':
            x = self.new_size[0]-self.size[0]
        else:
            x = (self.new_size[0]-self.size[0])/2

        if self.crop_method[1] == 'left':
            y = 0
        elif self.crop_method[1] == 'right':
            y = self.new_size[1]-self.size[1]
        else:
            y = (self.new_size[1]-self.size[1])/2

        thumb.paste(self.image, (int(x), int(y)))
        self.image = thumb

        self.size = [i for i in self.image.size]

    def _resize(self):
        if self.resize_method == 'scale':
            res = max(min(self.new_size[0], self.size[0])/self.size[0],
                      min(self.new_size[1], self.size[1])/self.size[1])
            new_size = [int(math.floor(self.size[0]*res)),
                        int(math.floor(self.size[1]*res))]
        elif self.resize_method == 'inscribe':
            res = min(min(self.new_size[0], self.size[0])/self.size[0],
                      min(self.new_size[1], self.size[1])/self.size[1])
            new_size = [int(math.floor(self.size[0]*res)),
                        int(math.floor(self.size[1]*res))]
        elif self.resize_method == 'stretch':
            new_size = self.new_size
        else:
            new_size = self.new_size
        self.image = self.image.resize(new_size, resample=Image.ANTIALIAS)
        self.size = [i for i in self.image.size]

    # свойства
    def _cm(self, crop_method):
        self.crop_method = crop_method.split(' ')

    def _rm(self, resize_method):
        self.resize_method = resize_method

    def _s(self, size):
        new_size = re.compile(r'(\d+)x(\d+)')
        self.new_size = new_size.search(size).groups()
        self.new_size = [float(i) for i in self.new_size]
        self.new_size[0] = int(self.new_size[0] if self.new_size[0] else
                               self.new_size[1]*self.size[0]/self.size[1])
        self.new_size[1] = int(self.new_size[1] if self.new_size[1] else
                               self.new_size[0]*self.size[1]/self.size[0])

    def _q(self, quality):
        self.quality = int(quality)

    def _c(self, color):
        tmp = tuple()
        for i in color.split(' '):
            tmp += (int(i), )
        self.color = tmp

    # готовые решения
    def _thumbnail(self):
        pass

    def get_thumbnail_url(self):
        if getattr(self, '_thumbnail_url', None) is None:
            self._thumbnail_url = "%s%s" % (
                self.store_url,
                os.path.basename(self.thumbnail_filename)
            )
        return self._thumbnail_url
    thumbnail_url = property(get_thumbnail_url)


def _dummyimage(task_list):
    if settings.DEBUG:
        task_list.reverse()
        final_size = re.compile(r's:(\d+)x(\d+)')
        for task in task_list:
            try:
                size = final_size.search(task).groups()
                break
            except AttributeError:
                pass
        return u'http://dummyimage.com/%sx%s/9e9e9e/424242.png' % size
    return '%simages/noise.png' % settings.STATIC_URL
    # return '%simages/none.gif' % settings.STATIC_URL


def get_thumbnail(filename, task_list):
    if type(task_list) in [str, unicode]:
        task_list = task_list.split(',')
    url = ''
    if os.path.isfile(filename):
        try:
            thumb = Thumbnail(filename, task_list)
            url = thumb.thumbnail_url
        except Exception, er:
            # TODO 1: log error message cuz noone wishes to debug till here
            # TODO 2: Если в размерах ноль при ошибке нет превьюшки
            logging.error(Exception)
            logging.error(er)
            url = _dummyimage(task_list)
    else:
        logging.error(u'File \'%s\' not find' % filename)
        # находить последний размер и цвет фона
        url = _dummyimage(task_list)
        # return ''
    return url
