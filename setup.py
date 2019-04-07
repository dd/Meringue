#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from setuptools import find_packages, setup
import codecs


long_description = '\n'.join([
    open(Path(__file__).parent / 'README.md').read(),
])


setup(
    name = 'Meringue',
    version = __import__('meringue').version,
    url = 'http://code.weboven.net/weboven_team/meringue',
    author = 'weboven team',
    author_email = 'dd@weboven.net',
    description = 'set of utilities for Django Framework',
    license = 'GNU GPL v3',
    packages = find_packages(),
    include_package_data = True,
    zip_safe = False,
    install_requires = [
        'Django>=2.1.7',
    ],
    extras_require = {
        'pillow': [
            'Pillow==5.4.1',
        ],
        # 'crypto': [
        #     'pycrypto==2.6.1',
        # ],
        # 'openpyxl': [
        #     'openpyxl==2.6.1',
        # ],
        'phonenumbers': [
            'phonenumbers==8.10.8',
        ],
        # 'django-pipeline': [
        #     'django-pipeline==1.6.14',
        #     'django-pipeline-browserify==0.6.2',
        # ],
    },
    long_description = long_description,
    platforms = 'All',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later \
(GPLv3+)',
        'Operating System :: OS Independent',
        'Natural Language :: Russian',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ]
)
