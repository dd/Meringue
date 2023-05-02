import logging
import os.path
import re
from hashlib import md5

from django.conf import settings as django_settings

import six
from PIL import Image

from meringue.conf import settings
from .methods import method_list
from .properties import property_list


logger = logging.getLogger("meringue")


property_list.update(settings.THUMBNAIL_PROPERTIES)
method_list.update(settings.THUMBNAIL_METHODS)


class Thumbnail:
    options = {
        "crop_method": settings.THUMBNAIL_CROP_METHOD,
        "resize_method": settings.THUMBNAIL_RESIZE_METHOD,
        "quality": settings.THUMBNAIL_QUALITY,
        "color": settings.THUMBNAIL_COLOR,
        "bg_color": settings.THUMBNAIL_BG_COLOR,
        "max_width": None,
        "max_height": None,
    }
    store_dir = settings.THUMBNAIL_DIR
    store_url = settings.THUMBNAIL_URL

    def __init__(self, filename, proc="extra@1"):
        if os.path.isabs(filename):
            self.filename = filename
        else:
            self.filename = os.path.join(django_settings.MEDIA_ROOT, filename)

        if not os.path.isfile(os.path.realpath(self.filename)):
            raise Exception("File '%s' does not exist." % filename)

        self.proc = proc
        if not self.is_valid_thumbnail():
            self.make_thumbnail()
        else:
            self.image = Image.open(self.thumbnail_filename)

    def is_valid_thumbnail(self):
        """
        проверяет существование и актуальность превью.
        """
        if not settings.THUMBNAIL_DEBUG and os.path.isfile(self.thumbnail_filename):
            return os.path.getmtime(self.filename) < os.path.getmtime(self.thumbnail_filename)
        return False

    def get_thumbnail_filename(self):
        if getattr(self, "_thumbnail_filename", None) is None:
            filename = f"{self.get_hash()}.png"
            if not os.path.exists(self.store_dir):
                os.mkdir(self.store_dir)
            self._thumbnail_filename = os.path.join(self.store_dir, filename)
        return self._thumbnail_filename

    thumbnail_filename = property(get_thumbnail_filename)

    def get_hash(self):
        """
        Указывать конечный размер?? зачем?
        """
        task_hash = self.proc
        if isinstance(task_hash, str):
            task_hash = [task_hash]  # self.proc
        task_hash.append(os.path.basename(self.filename))
        return md5(str(task_hash).encode()).hexdigest()  # noqa: S324

    def make_thumbnail(self):
        # try:
        self.image = Image.open(self.filename)
        self.image = self.image.convert("RGBA")
        # except IOError, detail:
        #     raise Exception(detail)

        self.options["current_size"] = [float(i) for i in self.image.size]
        self.options["new_size"] = [float(i) for i in self.image.size]

        logger.info("make thumbnail with tasks: %s" % ", ".join(self.proc))
        for proc in self.proc:
            if ":" in proc:
                prop, args = proc.split(":")
                self.options.update(property_list[prop](args, self.options))

            elif proc in method_list:
                self.image = method_list[proc](self.image, self.options)

        self.image.save(
            self.thumbnail_filename,
            "PNG",
            quality=self.options["quality"],
            optimize=1,
        )

    # # готовые решения
    # def _thumbnail(self):
    #     pass

    def get_thumbnail_url(self):
        if getattr(self, "_thumbnail_url", None) is None:
            self._thumbnail_url = f"{self.store_url}{os.path.basename(self.thumbnail_filename)}"
        return self._thumbnail_url

    thumbnail_url = property(get_thumbnail_url)


def _dummyimage(task_list):
    if django_settings.DEBUG:
        task_list.reverse()
        final_size = re.compile(r"s:(\d+)x(\d+)")
        for task in task_list:
            try:
                size = final_size.search(task).groups()
                break
            except AttributeError:
                pass
        # TODO: BUG: size could be undefined
        return f"http://dummyimage.com/{size}x{size}/9e9e9e/424242.png"

    return "%simages/noise.png" % django_settings.STATIC_URL
    # return '%simages/none.gif' % django_settings.STATIC_URL


def get_thumbnail(filename, task_list):
    if isinstance(task_list, six.string_types):
        task_list = task_list.split(",")

    url = ""
    if os.path.isfile(filename):
        thumb = Thumbnail(filename, task_list)
        url = thumb.thumbnail_url
        # try:
        # except Exception, er:
        #     # TODO 1: log error message cuz noone wishes to debug till here
        #     # TODO 2: Если в размерах ноль при ошибке нет превьюшки
        #     logger.error(Exception)
        #     logger.error(er)
        #     url = _dummyimage(task_list)
    else:
        logger.error("File '%s' not found" % filename)
        # находить последний размер и цвет фона
        url = _dummyimage(task_list)
        # return ''
    return url
