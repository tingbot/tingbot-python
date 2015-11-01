#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    # TODO: put package requirements here
]

setup(
    name='tingbot',
    version='0.2.3',
    description="Python APIs to write apps for Tingbot",
    long_description=readme,
    author="Joe Rickerby",
    author_email='joerick@mac.com',
    url='https://github.com/joerick/tingbot',
    packages=[
        'tingbot',
    ],
    package_dir={'tingbot':
                 'tingbot'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='tingbot',
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
    ],
)
