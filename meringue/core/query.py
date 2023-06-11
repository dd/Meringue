from django.db.models import Q
from django.db.models.query import QuerySet
from django.utils import timezone


class PublicationQuerySet(QuerySet):

    def published(self, *args, **kwargs):
        kwargs["is_published"] = True
        return self.filter(*args, **kwargs)

    def unpublished(self, *args, **kwargs):
        kwargs["is_published"] = False
        return self.filter(*args, **kwargs)


class PublicationDatesQuerySet(QuerySet):

    def published(self, *args, **kwargs):
        now = timezone.localtime()
        args = args + (
            Q(date_from__lt=now, date_to__gte=now) | \
            Q(date_from__isnull=True, date_to__gte=now) | \
            Q(date_from__lt=now, date_to__isnull=True) | \
            Q(date_from__isnull=True, date_to__isnull=True),
        )
        return self.filter(*args, **kwargs)

    def unpublished(self, *args, **kwargs):
        now = timezone.localtime()
        args = args + (Q(date_from__gte=now) | Q(date_to__lt=now))
        return self.filter(*args, **kwargs)
