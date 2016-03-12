# -*- coding: utf-8 -*-

import logging  # noqa

from django.core.files import uploadhandler

from . import settings as meringue_settings


# def _rename(d, rn):
#     return u'{0}{1}'.format(sha256(d).hexdigest(), os.path.splitext(rn)[1])


class MemoryFileUploadHandler(uploadhandler.MemoryFileUploadHandler):
    def file_complete(self, file_size):
        result = super(MemoryFileUploadHandler, self).file_complete(file_size)
        result.name = meringue_settings.UPLOAD_HANDLER_RENAME_FN(result)
        result.file.seek(0)
        return result


class TemporaryFileUploadHandler(uploadhandler.TemporaryFileUploadHandler):
    def file_complete(self, file_size):
        result = super(TemporaryFileUploadHandler, self).\
            file_complete(file_size)
        result.name = meringue_settings.UPLOAD_HANDLER_RENAME_FN(result)
        result.file.seek(0)
        return result
