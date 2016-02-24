dist: clean
	python setup.py sdist bdist_wheel

publish: dist
	twine upload -s dist/*

clean:
	rm -rf *.egg-info
	rm -rf dist

.PHONY: dist publish clean
