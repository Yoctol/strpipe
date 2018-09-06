.DEFAULT_GOAL := all

.PHONY: installself
installself:
	python setup.py build_ext
	pip install -e .

.PHONY: install
install:
	pip install -U pip wheel setuptools cython
	pip install -r requirements.txt
	make installself

.PHONY: lint
lint:
	flake8
	flake8 --config=.flake8.cython

.PHONY: test
test:
	pytest

.PHONY: all
all: test lint

.PHONY: clean
clean:
	rm -rf `find . -name __pycache__`
	rm -f `find . -type f -name '*.py[co]' `
	rm -f `find . -type f -name '*~' `
	rm -f `find . -type f -name '.*~' `
	rm -rf .cache
	rm -rf htmlcov
	rm -rf *.egg-info
	rm -f .coverage
	rm -f .coverage.*
	rm -rf build
	make -C docs clean
	python setup.py clean

.PHONY: dev-test
dev-test:
	rm -rf build
	python setup.py build_ext
	pip install -e .
	make lint
	pytest -v

.PHONY: docs
docs:
	make installself
	make -C docs
