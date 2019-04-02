# -*- coding: utf-8 -*-

import logging  # noqa


__VERSION__ = (
    (0, 4, 1),
    ('b', 5),
    # ('dev', 2)
)

try:
    from verlib import NormalizedVersion
    version = str(NormalizedVersion.from_parts(*__VERSION__))
except ImportError:
    version = '.'.join([str(j) for i in __VERSION__ for j in i])
