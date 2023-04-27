# -*- coding: utf-8 -*-

from django.db.models.manager import Manager

from meringue.core.query import PublishQuerySet


class PublishManager(Manager):
    use_for_related_fields = True

    def get_queryset(self):
        return PublishQuerySet(self.model, using=self._db)

    def published(self, *args, **kwargs):
        return self.get_queryset().published(*args, **kwargs)

    def unpublished(self, *args, **kwargs):
        return self.get_queryset().unpublished(*args, **kwargs)
