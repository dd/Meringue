class FileNotFindError(Exception):

    def __init__(self, file):
        message = f'Static file \"{file}\" not find'
        super().__init__(message)
