# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import logging  # noqa

from verlib import NormalizedVersion

__VERSION__ = (
    (0, 3, 5),
    # ('a', 1),
    # ('dev', 2)
)

version = str(NormalizedVersion.from_parts(*__VERSION__))
