# -*- coding: utf-8 -*-

from wo_sheet_pan import __VERSION__

from setuptools import setup, find_packages


version = '.'.join([str(v) for v in __VERSION__])

setup(
    name = 'wo_sheet_pan',
    description = '''Weboven django base package''',
    license = 'GNU GPL v3',
    version = version,
    author='Dmitriy Dobrynin',
    author_email='dd@weboven.net',
    install_requires = [
        'Django>=1.5.0',
        'South>=0.8.0',
        'pillow>=2.0.0',
    ],
    packages = find_packages(),
    include_package_data=True,
    zip_safe=True,
)
