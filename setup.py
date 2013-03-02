#!/usr/bin/env python
"""
sourcemap
=========

Parse JavaScript sourcemaps.
"""

from setuptools import setup, find_packages

install_requires = []
tests_require = []

setup(
    name='sourcemap',
    version='0.0.0',
    author='Matt Robenolt',
    author_email='matt@ydekproductions.com',
    url='https://github.com/mattrobenolt/python-sourcemap',
    description='Parse JavaScript sourcemaps.',
    long_description=__doc__,
    packages=find_packages(),
    install_requires=install_requires,
    tests_require=tests_require,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)
