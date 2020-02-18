.PHONY: clean test lint docs

JOBS ?= 1

help:
	@echo "make"
	@echo "    clean"
	@echo "        Remove Python/build artifacts."
	@echo "    formatter"
	@echo "        Apply black formatting to code."
	@echo "    lint"
	@echo "        Lint code with flake8, and check if black formatter should be applied."
	@echo "    types"
	@echo "        Check for type errors using pytype."
	@echo "    prepare-tests-ubuntu"
	@echo "        Install system requirements for running tests on Ubuntu and Debian based systems."
	@echo "    prepare-tests-macos"
	@echo "        Install system requirements for running tests on macOS."
	@echo "    prepare-tests-files"
	@echo "        Download all additional project files needed to run tests."
	@echo "    test"
	@echo "        Run pytest on tests/."
	@echo "        Use the JOBS environment variable to configure number of workers (default: 1)."

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f  {} +
	rm -rf build/
	rm -rf .pytype/
	rm -rf dist/
	rm -rf docs/_build

formatter:
	isort -rc -q david tests
	autoflake -i -r --remove-all-unused-imports --ignore-init-module-imports --remove-unused-variables david tests
	black david tests

lint:
	isort -rc -q -c david tests
	autoflake -i -r --remove-all-unused-imports --ignore-init-module-imports --remove-unused-variables -c david tests
	black --check david tests
	flake8 david tests

types:
	pytype --keep-going david

docs: 
	cd docs/ && $(MAKE) html && cd ..

prepare-tests-macos: prepare-wget-macos prepare-tests-files
	brew install graphviz || true

prepare-wget-macos:
	brew install wget || true

prepare-tests-ubuntu: prepare-tests-files
	sudo apt-get -y install graphviz graphviz-dev python3-tk

prepare-tests-files:

test: clean
	coverage run -m  pytest tests

coverage: test
	coverage xml

#release:
#	python3 scripts/release.py
