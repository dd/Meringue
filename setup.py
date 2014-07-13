# -*- coding: utf-8 -*-

import meringue#  __VERSION__

from setuptools import setup, find_packages


# version = '.'.join([str(v) for v in __VERSION__])

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
        'South>=0.8.0',
        'pillow>=2.0.0',
        'verlib',
    ],
    packages = find_packages(),
    include_package_data = True,
    zip_safe = True,
    platforms = 'All',
    long_description = '\n%s' % open('README.rst').read(),
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
