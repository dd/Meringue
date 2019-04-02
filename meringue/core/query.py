# -*- coding: utf-8 -*-

from django.db.models.query import QuerySet


class PublishQuerySet(QuerySet):
    use_for_related_fields = True

    def published(self, *args, **kwargs):
        kwargs.update({
            'is_published': True
        })
        return self.filter(*args, **kwargs)

    def unpublished(self, *args, **kwargs):
        kwargs.update({
            'is_published': False
        })
        return self.filter(*args, **kwargs)
