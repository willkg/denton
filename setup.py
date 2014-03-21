#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
from setuptools import setup, find_packages


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')


def get_version():
    VERSIONFILE = os.path.join('denton', '__init__.py')
    VSRE = r"""^__version__ = ['"]([^'"]*)['"]"""
    version_file = open(VERSIONFILE, 'rt').read()
    return re.search(VSRE, version_file, re.M).group(1)


setup(
    name='denton',
    version=get_version(),
    description='System for emailing weekly reports with data derived from '
                'JSON API endpoints',
    long_description=readme + '\n\n' + history,
    author='Will Kahn-Greene',
    author_email='willkg@bluesock.org',
    url='https://github.com/willkg/denton',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': ['denton-cmd = denton.main:main'],
    },
    install_requires=[
        'requests',
    ],
    license="BSD",
    zip_safe=True,
    keywords='',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    test_suite='tests',
)
