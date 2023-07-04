from django.db import models
from django.utils.translation import gettext_lazy as _

from meringue.core.managers import PublicationDatesManager
from meringue.core.managers import PublicationManager
from meringue.core.managers import SortingManager


class CMTimeMixin(models.Model):
    """
    A simple mixin to add _ctime_ and _mtime_ fields.
    """

    ctime = models.DateTimeField(auto_now_add=True, help_text=_("Date and time of creation."))
    mtime = models.DateTimeField(auto_now=True, help_text=_("Date and time of editing."))

    class Meta:
        abstract = True


class SortingMixin(models.Model):
    """
    Simple mixin to add sorting field.
    """

    sorting = models.SmallIntegerField(
        verbose_name=_("Sorting"),
        help_text=_("Sorting order."),
        default=0,
    )

    objects = SortingManager()

    class Meta:
        ordering = [
            "sorting",
        ]
        abstract = True


class PublicationMixin(models.Model):
    """
    Mixin with the functionality of manual publishing.

    Examples:
        >>> FooModel.object.published()
        >>> FooModel.object.unpublished()
    """

    is_published = models.BooleanField(
        verbose_name=_("Publication"),
        help_text=_("Show/Hide"),
        default=True,
        db_index=True,
    )

    objects = PublicationManager()

    class Meta:
        abstract = True


class PublicationDatesMixin(models.Model):
    """
    Mixin with the functionality of publishing in a certain period.

    Examples:
        >>> FooModel.object.published()
        >>> FooModel.object.unpublished()
    """

    date_from = models.DateTimeField(
        verbose_name=_("Date from"),
        help_text=_("Date and time of publication (inclusive)."),
        blank=True,
        null=True,
    )
    date_to = models.DateTimeField(
        verbose_name=_("Date to"),
        help_text=_("Date and time when to hide."),
        blank=True,
        null=True,
    )

    objects = PublicationDatesManager()

    class Meta:
        abstract = True
