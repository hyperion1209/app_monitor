PACKAGE = $(shell python setup.py --name)

FWDPORT ?= 8000

define NO_VENV_ERROR_MESSAGE
You need to have a Python VirtualEnv enabled.

For help on how to set one up see https://wolinks.com/netauto_env_setup
endef


.PHONY: check_venv
check_venv:
ifndef VIRTUAL_ENV
	$(error $(NO_VENV_ERROR_MESSAGE) )
endif

.PHONY: dev
dev: check_venv
	@echo "Setting up development environment for ${PACKAGE}"
	@pip install --disable-pip-version-check -e .[dev]

.PHONY: shell
shell: check_venv
	@python -m IPython

.PHONY: clean
clean: check_venv
	-@pip uninstall --disable-pip-version-check -y ${PACKAGE} > /dev/null 2>&1
	-@rm -rf src/${PACKAGE}.egg-info src/app_monitor/_version.py
	-@rm -rf .eggs
	-@rm -rf src/${PACKAGE}/__pycache__

.PHONY: fmt
fmt: check_venv
	python -m black --target-version py36 --line-length 80 .

.PHONY: lint
lint: check_venv
	python -m flake8 --exit-zero src
	python -m mypy src

.PHONY: test
test: check_venv
	@python -m pytest -v

.PHONY: docs
docs: check_venv
	@mkdocs serve -a 0.0.0.0:$(FWDPORT)
