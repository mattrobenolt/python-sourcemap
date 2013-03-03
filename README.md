# Sourcemap
Parse JavaScript sourcemaps.

```python
>>> import sourcemap
>>> sourcemap.discover('...')
'jquery.min.map'
>>> tokens = sourcemap.loads('...')
>>> tokens.lookup(line=10, column=10)
<Token: dst_line=10 dst_column=10 src='jquery.js' src_line=50 src_col=200 name='lol'>
```
