from django.db.models import Q
from django.db.models.query import QuerySet
from django.utils import timezone


class SortingQuerySet(QuerySet):
    def correction_sorting(self):
        """
        This is a method to update/fix the sorting of the selected list of items.

        The sorting will be done according to the `queryset` sorting, so sorting can be controlled
        by executing `.order_by()` before calling the `correction_sorting` method.

        The selection for updating sorting can be pre-limited by filtering the list.
        """
        items = []
        sorting = 0
        for item in self:
            if item.sorting != sorting:
                item.sorting = sorting
                items.append(item)
            sorting += 1

        return self.bulk_update(items, ["sorting"])


class PublicationQuerySet(QuerySet):
    def published(self, *args, **kwargs):
        """
        Method to getting published items.
        """
        kwargs["is_published"] = True
        return self.filter(*args, **kwargs)

    def unpublished(self, *args, **kwargs):
        """
        Method for getting unpublished items.
        """
        kwargs["is_published"] = False
        return self.filter(*args, **kwargs)


class PublicationDatesQuerySet(QuerySet):
    def published(self, *args, **kwargs):
        """
        Method to getting published items.
        """
        now = timezone.localtime()
        args = (
            *args,
            Q(date_from__lte=now, date_to__gt=now)
            | Q(date_from__isnull=True, date_to__gt=now)
            | Q(date_from__lte=now, date_to__isnull=True)
            | Q(date_from__isnull=True, date_to__isnull=True),
        )
        return self.filter(*args, **kwargs)

    def unpublished(self, *args, **kwargs):
        """
        Method for getting unpublished items.
        """
        now = timezone.localtime()
        args = (*args, Q(date_from__gt=now) | Q(date_to__lte=now))
        return self.filter(*args, **kwargs)
