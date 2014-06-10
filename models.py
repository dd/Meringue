# -*- coding: utf-8 -*-

import re

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
    'namespace',
    'url_name',
    'reverse_args',
)


##########
# mixins #
##########

class GetAbsoluteUrlMixin(object):

    def get_absolute_url(self):
        url_name = getattr(self._meta, 'url_name', None)
        if not url_name:
            cls = self.__class__.__name__.lower()
            url_name = '%s_detail' % cls

        namespace = getattr(self._meta, 'namespace', None)
        if not namespace:
            s = self.__module__
            r = r'(.+)\.models$'
            namespace = re.findall(r, s)[0].lower().replace('.', '_')

        url = '%s:%s' % (namespace, url_name)

        if hasattr(self._meta, 'reverse_args'):
            reverse_args = [getattr(self, key) for key in
                            self._meta.reverse_args]
        else:
            reverse_args = [str(self.id)]

        if 'django_hosts' in settings.INSTALLED_APPS:
            s = self.__module__
            r = r'(.[^\.]+).+\.models$'
            module_name = re.findall(r, s)[0]
            if hasattr(self._meta, 'host_name'):
                host_name = self._meta.host_name
            else:
                module = __import__(module_name)
                host_name = getattr(module, 'host_name', module_name)
            return reverse_full(host=host_name, view=url,
                                view_args=reverse_args)

        return reverse(url, args=reverse_args)


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
    is_published = models.BooleanField(
        verbose_name=_(u'публикация'),
        help_text=_(u'Отображать/Скрыть'),
        default=True,
        db_index=True,
    )

    objects = PublishManager()

    class Meta:
        abstract = True
