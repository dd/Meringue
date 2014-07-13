# -*- coding: utf-8 -*-

from wo_sheet_pan import __VERSION__

from setuptools import setup, find_packages


version = '.'.join([str(v) for v in __VERSION__])

setup(
    name = 'wo_sheet_pan',
    description = '''Weboven django base package''',
    version = version,
    license = 'GNU GPL v3',
    author = 'weboven team',
    author_email = 'dd@weboven.net',
    url = 'https://github.com/dd/wo-sheet-pan',
    install_requires = [
        'Django>=1.5.0',
        'South>=0.8.0',
        'pillow>=2.0.0',
    ],
    packages = find_packages(),
    include_package_data = True,
    zip_safe = True,
    platforms = 'All',
    long_description = '\n%s' % open('README.md').read(),
)
