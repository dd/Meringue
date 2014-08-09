# -*- coding: utf-8 -*-

import logging
try:
    from verlib import NormalizedVersion
except ImportError:
    pass


def get_version(version):
    try:
        return str(NormalizedVersion.from_parts(*version))
    except NameError:
        logging.info(u'for better install verlib' )
        return '.'.join([str(j) for i in version for j in i])
