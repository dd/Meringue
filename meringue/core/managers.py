# -*- coding: utf-8 -*-

import logging  # noqa

from django.db.models.manager import Manager


logger = logging.getLogger('meringue')


class PublishManager(Manager):
    use_for_related_fields = True

    def published(self, *args, **kwargs):
        kwargs.update({
            'is_published': True
        })
        return self.get_queryset().filter(*args, **kwargs)
