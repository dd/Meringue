# -*- coding: utf-8 -*-


class FileNotFindError(Exception):

    def __init__(self, file):
        message = "Static file \"{file}\" not find".format(file=file)
        super(FileNotFindError, self).__init__(message)
