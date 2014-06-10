# -*- coding:utf-8 -*-

import re


class UrlPatterns(object):

    '''
        Возвращает патерн урлов с прописанным приложением и пространством имён
    '''

    def __init__(self, namespace=None, app_name=None):
        if not app_name:
            s = self.__module__
            r = r'([^\.]+)'
            app_name = '_'.join(re.findall(r, s)[:-1]).lower()
        if not namespace:
            namespace = app_name

        self.app_name = app_name
        self.namespace = namespace

    def __call__(self):
        return self.get_urlpatterns(), self.app_name, self.namespace

    def get_urlpatterns(self):
        return self.urlpatterns
