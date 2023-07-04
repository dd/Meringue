from django.db.models import Manager

from meringue.core.query import PublicationDatesQuerySet
from meringue.core.query import PublicationQuerySet
from meringue.core.query import SortingQuerySet


class SortingManager(Manager):
    """
    Manager with sorting correction functionality.
    """

    def get_queryset(self):
        return SortingQuerySet(model=self.model, using=self._db, hints=self._hints)

    def correction_sorting(self):
        return self.get_queryset().correction_sorting()


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
