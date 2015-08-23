#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
from os.path import dirname, join

from setuptools import find_packages, setup

long_description = '\n'.join([
    open(join(dirname(__file__), 'README.rst')).read(),
    # open(join(dirname(__file__), 'CHANGELOG.rst')).read()
])

requirements_path = 'requirements.txt'
with codecs.open(join(dirname(__file__),
                      requirements_path)) as requirements_file:
    requirements = requirements_file.read().split('\n')

setup(
    name = 'Meringue',
    version = __import__('meringue').version,
    url = 'https://github.com/dd/Meringue',
    author = 'weboven team',
    author_email = 'dd@weboven.net',
    description = 'set of utilities for Django Framework',
    license = 'GNU GPL v3',
    packages = find_packages(),
    include_package_data = True,
    zip_safe = False,
    install_requires = requirements,
    setup_requires=[
        'flake8',
        'isort',
    ],
    long_description = long_description,
    platforms = 'All',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later \
(GPLv3+)',
        'Operating System :: OS Independent',
        'Natural Language :: Russian',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
