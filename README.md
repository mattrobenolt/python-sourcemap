Rollbar Info
============

This is a private clone of https://github.com/mattrobenolt/python-sourcemap
so we can build package distributions from it pinned to the version we use.

As of 2022-12-02, there should be a version on our Python private registry built and ready to use:
https://console.cloud.google.com/artifacts/python/rollbar-prod/us-central1/python-private-registry/sourcemap?project=rollbar-prod

This corresponds to the commit pinned as a dependency for mox at the time of writing: `05735efbd5c8cdcaff0c2ca3b341dafc3d1dbadb`
And it's marked as `0.3.0+05735ef`.

It has been build following this procedure, which can be replicated if we ever need to switch to a more recent version or push a patch to it.
You'll need a service account that has the `roles/artifactregistry.writer`.  This is needed for Python2, as we cannot use the keyring auth provider.
With that, you can see the config needed for twine.
Execute this command:

```
gcloud artifacts print-settings python \
  --repository=python-private-registry \
  --project=rollbar-prod \
  --location=us-central1 \
  --json-key=/path/to/my-sa-key.json
```

That will produce something like this:
```
# Insert the following snippet into your .pypirc

[distutils]
index-servers =
    python-private-registry

[python-private-registry]
repository: https://us-central1-python.pkg.dev/rollbar-prod/python-private-registry/
username: _json_key_base64
password: ...

# Insert the following snippet into your pip.conf

[global]
extra-index-url = https://_json_key_base64:...@us-central1-python.pkg.dev/rollbar-prod/python-private-registry/simple/
```

We're only interested on the username and password of the registry.  Copy those somewhere.

Now:

- checkout the repo to the commit or tag you need
- modify `sourcemap/__init__.py` to reflect the new version.  Always
  append the `+HASH` to the version in order not to conflict with upstream.
- launch a shell into a docker image with Python 2.7 support (password is the base64 string from before):
  `docker run -ti --rm -v $(pwd):/app -e TWINE_USERNAME=_json_key_base64 -e TWINE_PASSWORD=<...> cimg/python:2.7 /bin/bash`
- launch the included `./tools/build_and_publish.sh` script

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
 * Python 2.6
 * Python 2.7
 * Python 3.3
 * Python 3.4
 * Python 3.5
 * PyPy
 * PyPy3
