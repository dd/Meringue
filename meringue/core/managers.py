from django.db.models.manager import Manager

from meringue.core.query import PublicationQuerySet
from meringue.core.query import PublicationDatesQuerySet


class PublicationManager(Manager):

    def get_queryset(self):
        return PublicationQuerySet(self.model, using=self._db)

    def published(self, *args, **kwargs):
        return self.get_queryset().published(*args, **kwargs)

    def unpublished(self, *args, **kwargs):
        return self.get_queryset().unpublished(*args, **kwargs)


class PublicationDatesManager(Manager):

    def get_queryset(self):
        return PublicationDatesQuerySet(self.model, using=self._db)

    def published(self, *args, **kwargs):
        return self.get_queryset().published(*args, **kwargs)

    def unpublished(self, *args, **kwargs):
        return self.get_queryset().unpublished(*args, **kwargs)
