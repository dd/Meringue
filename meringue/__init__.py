# -*- coding: utf-8 -*-


def get_version(raw_version):
    # https://www.python.org/dev/peps/pep-0386/#the-new-versioning-algorithm

    version = ""
    for subversion in raw_version:

        if subversion[0] in ['a', 'b', 'c', 'rc']:
            # [{a|b|c|rc}N[.N]+]
            version += f'{subversion[0]}{subversion[1]}'
            if len(subversion) == 3:
                version += f'.{subversion[2]}'

        elif subversion[0] in ['post', 'dev']:
            # [.postN][.devN]
            version += f'.{subversion[0]}{subversion[1]}'

        else:
            # N.N[.N]
            version = '.'.join([str(i) for i in subversion])
    return version


version = __VERSION__ = get_version((
    (0, 4, 1),
    ('b', 15),
    # ('dev', 2)
))
