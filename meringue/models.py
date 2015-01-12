# -*- coding: utf-8 -*-

from django.conf import settings
from django.db import models
from django.db.models.query import QuerySet
from django.utils.translation import ugettext_lazy as _
import django.db.models.options as options

if 'django_hosts' in settings.INSTALLED_APPS:
    from django_hosts.reverse import reverse_full
else:
    from django.core.urlresolvers import reverse


options.DEFAULT_NAMES = options.DEFAULT_NAMES + (
    'host_name',
    'view',
    'reverse_args',
)


##########
# mixins #
##########

class GetAbsoluteUrlMixin(object):

    '''
        Миксин автоматизирующий получение абсолютного адреса
        Для получения адреса использует стандартную функцию reverse (в
    случае если установлен django_hosts то reverse_full)

        При реверсе предполагается следующая схема:

            * host_name - название верхнего модуля в нижнем регистре
        (используется в случае установенного django_hosts)

            * view - '<namespace>:<url_name>':
                - namespace - название приложения приведённое к нижнему
            регистру и точки заменённые на нижнее подчёркивание
                - url_name - название класса приведённое к нижнему регистру
            с приставкой '-detail'

            * args - по умолчанию pk модели

        При определении класса модели можно предустановить параметры:
            * host_name - название целевого хоста (string)
            * view - целевой url (string)
            * reverse_args - список атрибутов модели (list)
    '''

    def _host_name(self):
        if not hasattr(self._meta, 'host_name'):
            module_name = self.__module__.split('.')[0]
            module = __import__(module_name)
            self._meta.host_name = getattr(module, 'host_name',
                                           module_name.lower())
        return self._meta.host_name

    def _view(self):
        if not hasattr(self._meta, 'view'):
            namespace = self.__module__[:-7].lower().replace('.', '_')

            cls = self._meta.model_name
            view = '%s-detail' % cls

            self._meta.view = '%s:%s' % (namespace, view)
        return self._meta.view

    def _reverse_args(self):
        reverse_args = getattr(self._meta, 'reverse_args', ['pk'])
        return [getattr(self, key) for key in reverse_args]

    def get_absolute_url(self):
        if 'django_hosts' in settings.INSTALLED_APPS:
            return reverse_full(host=self._host_name(),
                                view=self._view(),
                                view_args=self._reverse_args())
        return reverse(self._view(), args=self._reverse_args())


#############
# querysets #
#############

class PublishQuerySet(QuerySet):

    def published(self, **kwargs):
        return self.filter(is_published=True, **kwargs)


############
# managers #
############

class PublishManager(models.Manager):
    use_for_related_fields = True

    def get_query_set(self):
        return PublishQuerySet(self.model)

    def published(self, *args, **kwargs):
        return self.get_query_set().published(*args, **kwargs)


##########
# models #
##########

class PublishModel(GetAbsoluteUrlMixin, models.Model):

    '''
        Абстрактная модель с признаком публикации (поле is_published)
        менеджер имеет метод published() аналог стандартного filter() с
    заранее указанными is_published=True
        так же наследует GetAbsoluteUrlMixin
    '''

    is_published = models.BooleanField(
        verbose_name=_(u'публикация'),
        help_text=_(u'Отображать/Скрыть'),
        default=True,
        db_index=True,
    )

    objects = PublishManager()

    class Meta:
        abstract = True
