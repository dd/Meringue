# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import logging  # noqa

__VERSION__ = (
    (0, 3, 5),
    # ('a', 1),
    # ('dev', 2)
)

try:
    from verlib import NormalizedVersion
    version = str(NormalizedVersion.from_parts(*__VERSION__))
except ImportError:
    version = '.'.join([str(j) for i in __VERSION__ for j in i])
