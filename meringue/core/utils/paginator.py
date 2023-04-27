# -*- coding: utf-8 -*-

import logging  # noqa

from django.core.paginator import Paginator as DjPaginator


class Paginator(DjPaginator):
    """
    What?
    """

    def __init__(self, object_list, per_page, orphans=0,
                 allow_empty_first_page=True, reverse=False):
        super().__init__(object_list, per_page, orphans,
                         allow_empty_first_page)
        self.reverse = bool(reverse)

    def page(self, number):
        """Return a Page object for the given 1-based page number."""
        number = self.validate_number(number)

        bottom = (number - 1) * self.per_page
        top = bottom + self.per_page
        if top + self.orphans >= self.count:
            top = self.count

        if self.reverse:
            bottom, top = self.count - top, self.count - bottom

        return self._get_page(self.object_list[bottom:top], number, self)
