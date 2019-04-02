# -*- coding: utf-8 -*-

from django.core.files import uploadhandler

from meringue.conf import settings


class MemoryFileUploadHandler(uploadhandler.MemoryFileUploadHandler):
    def file_complete(self, file_size):
        result = super(MemoryFileUploadHandler, self).file_complete(file_size)
        if result:
            result.name = settings.UPLOAD_RENAME_HANDLER(result)
            result.file.seek(0)
        return result


class TemporaryFileUploadHandler(uploadhandler.TemporaryFileUploadHandler):
    def file_complete(self, file_size):
        result = super(TemporaryFileUploadHandler, self).\
            file_complete(file_size)
        if result:
            result.name = settings.UPLOAD_RENAME_HANDLER(result)
            result.file.seek(0)
        return result
