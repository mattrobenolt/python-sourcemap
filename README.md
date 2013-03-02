# Sourcemap
Parse JavaScript sourcemaps.

```python
>>> import sourcemap
>>> sourcemap.discover('...')
'jquery.min.map'
>>> map = sourcemap.loads('...')
>>> pointer = map.lookup(line=10, column=10)
{'file': 'jquery.js', 'line': 500, 'column': 20}
>>> map.get_file(pointer)
'The whole file...'
```
