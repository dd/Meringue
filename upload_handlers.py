# -*- coding: utf-8 -*-

import os.path
import uuid

from django.core.files import uploadhandler


def _rename(fn):
    return '%s%s' % (uuid.uuid4(), os.path.splitext(fn)[1])


class MemoryFileUploadHandler(uploadhandler.MemoryFileUploadHandler):
    def new_file(self, field_name, file_name, content_type,
                 content_length, charset=None):
        file_name = _rename(file_name)
        super(MemoryFileUploadHandler, self).new_file(
            field_name,
            file_name,
            content_type,
            content_length,
            charset
        )


class TemporaryFileUploadHandler(uploadhandler.TemporaryFileUploadHandler):
    def new_file(self, field_name, file_name, content_type, content_length,
                 charset=None):
        file_name = _rename(file_name)
        super(TemporaryFileUploadHandler, self).new_file(
            field_name,
            file_name,
            content_type,
            content_length,
            charset
        )
