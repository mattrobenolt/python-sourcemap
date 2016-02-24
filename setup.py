#!/usr/bin/env python
"""
SourceMap
~~~~~~~~~

Parse JavaScript source maps.

  >>> import sourcemap
  >>> sourcemap.discover('...')
  'jquery.min.map'
  >>> index = sourcemap.loads('...')
  >>> index.lookup(line=10, column=10)
  <Token: dst_line=10 dst_column=10 src='jquery.js' src_line=50 src_col=200 name='lol'>

:copyright: (c) 2013 by Matt Robenolt
:license: BSD, see LICENSE for more details.
"""
from setuptools import setup, find_packages
import re

# lol
version = re.search(r'__version__ = \'([^\']+)\'', open('sourcemap/__init__.py').read(), re.MULTILINE).groups()[0]

install_requires = []
tests_require = []

setup(
    name='sourcemap',
    version=version,
    author='Matt Robenolt',
    author_email='matt@ydekproductions.com',
    url='https://github.com/mattrobenolt/python-sourcemap',
    description='Parse JavaScript source maps.',
    long_description=__doc__,
    packages=find_packages(),
    install_requires=install_requires,
    tests_require=tests_require,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python',
        'Topic :: Software Development'
    ],
)
