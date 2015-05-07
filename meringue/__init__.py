# -*- coding: utf-8 -*-

__VERSION__ = (
    (0, 3, 2),
    # ('a', 3),
    # ('dev', 7)
)

try:
    from verlib import NormalizedVersion
    version = str(NormalizedVersion.from_parts(*__VERSION__))
except ImportError:
    version = '.'.join([str(j) for i in __VERSION__ for j in i])
