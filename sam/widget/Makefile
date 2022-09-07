.DEFAULT_GOAL := all
black = black --target-version py39 widget
isort = isort --profile black widget

FLEXDIR = ../../

.PHONY: format
format:
	$(isort)
	$(black)

.PHONY: lint
lint: setup-install
	flake8 --ignore=E203,F841,E501,E722,W503 widget
	$(isort) --check-only --df
	$(black) --check --diff

.PHONY: prepare
prepare:
	mkdir -p flex/python
	cp $(FLEXDIR)/setup.py flex/python
	cp -r $(FLEXDIR)/flex flex/python
	cp -r $(FLEXDIR)/example flex/python

.PHONY: build
build: prepare
	sam build

.PHONY: run
run:
	sam local invoke --force-image-build "WidgetFunction" -e events/event.json

.PHONY: all
all: build
	sam local invoke --force-image-build "WidgetFunction" -e events/event.json


.PHONY: clean
clean:
	python setup.py clean
	git status

.PHONY: tests
tests: format lint
	pytest

