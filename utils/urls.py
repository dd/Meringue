# -*- coding:utf-8 -*-


class UrlPatterns(object):

    '''
        Возвращает патерн урлов с прописанным приложением и пространством имён
    '''

    def __init__(self, namespace=None, app_name=None):
        self.app_name = app_name or '_'.join(self.__module__.split('.')[:-1]).lower()
        self.namespace = namespace or self.app_name

    def __call__(self):
        return self.get_urlpatterns(), self.app_name, self.namespace

    def get_urlpatterns(self):
        return self.urlpatterns
