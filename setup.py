#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    'pyzmq',
    'docopt',
    'virtualenv',
    'requests',
    'Pillow',
]

setup(
    name='tingbot-python',
    version='0.4.0',
    description="Python APIs to write apps for Tingbot",
    long_description=readme,
    author="Joe Rickerby",
    author_email='joerick@mac.com',
    url='https://github.com/tingbot/tingbot-python',
    packages=[
        'tingbot',
        'tbtool'
    ],
    package_dir={'tingbot': 'tingbot',
                 'tbtool': 'tbtool'},
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
    entry_points={
        'console_scripts': [
            'tbtool = tbtool.__main__:main',
        ],
    },
    test_suite='tests',
    tests_require=['httpretty','mock'],
)
