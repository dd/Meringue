# -*- coding: utf-8 -*-

import logging  # noqa

# from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

# if 'django_hosts' in settings.INSTALLED_APPS:
#     from django_hosts.resolvers import reverse
# else:
#     from django.urls import reverse

from .managers import PublishManager
# from meringue import configuration


logger = logging.getLogger('meringue')


##########
# mixins #
##########

class CMTimeMixin(models.Model):
    ctime = models.DateTimeField(auto_now_add=True)
    mtime = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SortingMixin(models.Model):
    sorting = models.SmallIntegerField(verbose_name=_('Порядок'),
                                       help_text=_('Порядок сортировки'),
                                       default=0, )
    class Meta:
        ordering = ['sorting', ]
        abstract = True


# class GetAbsoluteUrlMixin(object):

#     '''
#         Примесь автоматизирующая получение абсолютного адреса
#         Для получения адреса использует стандартную функцию reverse (в
#     случае если установлен django_hosts то reverse_full)

#         При реверсе предполагается следующая схема:

#             * host_name - название верхнего модуля в нижнем регистре
#         (используется в случае установенного django_hosts)

#             * view - '<namespace>:<url_name>':
#                 - namespace - название приложения приведённое к нижнему
#             регистру и точки заменённые на нижнее подчёркивание
#                 - url_name - название класса приведённое к нижнему регистру
#             с приставкой '-detail'

#             * args - по умолчанию pk модели

#         При определении класса модели можно предустановить параметры:
#             * host_name - название целевого хоста (string)
#             * view - целевой url (string)
#             * reverse_args - список атрибутов модели (list)
#     '''

#     def _host_name(self):
#         if not hasattr(self._meta, 'host_name'):
#             module_name = self.__module__.split('.')[0]
#             module = __import__(module_name)
#             self._meta.host_name = getattr(module, 'host_name',
#                                            module_name.lower())
#         return self._meta.host_name

#     def _view(self):
#         if not hasattr(self._meta, 'view'):
#             namespace = self.__module__[:-7].lower().replace('.', '_')

#             cls = self._meta.model_name
#             view = '%s-detail' % cls

#             self._meta.view = '%s:%s' % (namespace, view)
#         return self._meta.view

#     def _reverse_args(self):
#         reverse_args = getattr(self._meta, 'reverse_args', ['pk'])
#         return [getattr(self, key) for key in reverse_args]

#     def get_absolute_url(self):
#         reverse_args = {
#             'viewname': self._view(),
#             'args': self._reverse_args(),
#         }
#         if 'django_hosts' in settings.INSTALLED_APPS:
#             reverse_args.update({
#                 'host': self._host_name(),
#                 'port': configuration.PORT,
#             })
#         return reverse(**reverse_args)


###################
# Abstract models #
###################

class PublishedBase(models.Model):
    """
        publish abstract model
        managr has method published() like a filter()
    """

    is_published = models.BooleanField(
        verbose_name=_('публикация'),
        help_text=_('Отображать/Скрыть'),
        default=True,
        db_index=True,
    )

    objects = PublishManager()

    class Meta:
        abstract = True
