# -*- coding: utf-8 -*-

import os.path
try:
    from hashlib import md5
except ImportError:
    from md5 import md5

from django.core.files import uploadhandler


def _rename(v, rn):
    return u'{0}.{1}'.format(md5(v).hexdigest(), os.path.splitext(rn)[1])


class MemoryFileUploadHandler(uploadhandler.MemoryFileUploadHandler):
    def file_complete(self, file_size):
        self.file_name = _rename(self.file.getvalue(), self.file_name)
        return super(MemoryFileUploadHandler, self).file_complete(file_size)


class TemporaryFileUploadHandler(uploadhandler.TemporaryFileUploadHandler):
    def file_complete(self, file_size):
        self.file_name = _rename(self.file.getvalue(), self.file_name)
        return super(MemoryFileUploadHandler, self).file_complete(file_size)
