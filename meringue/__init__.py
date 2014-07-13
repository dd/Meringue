# -*- coding: utf-8 -*-

from verlib import NormalizedVersion

__VERSION__ = (
    (0, 3, 6),
)

version = str(NormalizedVersion.from_parts(*__VERSION__))
