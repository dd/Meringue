# -*- coding: utf-8 -*-

import meringue

from setuptools import setup, find_packages


long_description = '\n'.join([
    open('README.rst').read(),
    open('CHANGELOG.rst').read()
])

setup(
    name = 'Meringue',
    description = '''Weboven django base package''',
    version = meringue.version,
    license = 'GNU GPL v3',
    author = 'weboven team',
    author_email = 'dd@weboven.net',
    url = 'https://github.com/dd/Meringue',
    install_requires = [
        'Django>=1.5.0',
        'pillow>=2.0.0',
    ],
    packages = find_packages(),
    include_package_data = True,
    zip_safe = True,
    platforms = 'All',
    long_description = long_description,
    classifiers=[
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
