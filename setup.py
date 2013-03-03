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

install_requires = []
tests_require = []

setup(
    name='sourcemap',
    version='0.1.0',
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
        'Topic :: Software Development'
    ],
)
