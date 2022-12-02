#!/bin/sh

set -eu

cd /app || exit 1

# install the twine tool to upload the python distributions
pip install twine

# build the distributions:
python setup.py sdist bdist_wheel

# upload to registry
twine upload \
    --repository-url https://us-central1-python.pkg.dev/rollbar-prod/python-private-registry/ \
    --verbose \
    dist/*
