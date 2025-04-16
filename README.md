# SourceMap [![Build Status](https://travis-ci.org/mattrobenolt/python-sourcemap.png?branch=master)](https://travis-ci.org/mattrobenolt/python-sourcemap)
Parse JavaScript source maps.

*Based on [https://github.com/martine/python-sourcemap](https://github.com/martine/python-sourcemap)*

## Installation
`$ pip install sourcemap`

## Usage
### Overview
```python
>>> import sourcemap
>>> sourcemap.discover('...')
'jquery.min.map'
>>> index = sourcemap.loads('...')
>>> index.lookup(line=10, column=10)
<Token: dst_line=10 dst_column=10 src='jquery.js' src_line=50 src_col=200 name='lol'>
```

### Get lines of context
```python
# Load in our original minified file
>>> minified = open('jquery.min.js').read()
# Discover the path to the source map
>>> map_path = sourcemap.discover(minified)
# Read and parse our sourcemap
>>> index = sourcemap.load(open(map_path))
# Look up the line/column from the minified file
>>> token = index.lookup(line=0, column=3040)
# Grab the line from the original source that this token points to
>>> source = open('jquery.js').readlines()
>>> culprit = source[token.src_line]
# 5 lines before
>>> pre_context = source[token.src_line - 5:token.src_line]
# 5 lines after
>>> post_context = source[token.src_line + 1:token.src_line + 6]
```

### Compatibility
 * Python 3.9
 * Python 3.10
 * Python 3.11
 * Python 3.12
 * Python 3.13
 * PyPy 3.10
