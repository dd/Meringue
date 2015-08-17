#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
from os.path import join, dirname

from setuptools import setup, find_packages

import meringue


long_description = '\n'.join([
    open(join(dirname(__file__), 'README.rst')).read(),
    open(join(dirname(__file__), 'CHANGELOG.rst')).read()
])

requirements_path = 'requirements.txt'
with codecs.open(join(dirname(__file__),
                      requirements_path)) as requirements_file:
    requirements = requirements_file.read().split('\n')

setup(
    name = 'Meringue',
    description = '''Weboven django base package''',
    version = meringue.version,
    license = 'GNU GPL v3',
    author = 'weboven team',
    author_email = 'dd@weboven.net',
    url = 'https://github.com/dd/Meringue',
    install_requires = requirements,
    packages = find_packages(),
    include_package_data = True,
    zip_safe = False,
    platforms = 'All',
    long_description = long_description,
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
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