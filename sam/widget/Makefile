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

.PHONE: quote
quote:
	sam local invoke --force-image-build "QuoteFunction" -e events/quote.json

.PHONE: widget
widget:
	sam local invoke --force-image-build "WidgetFunction" -e events/widget.json

.PHONY: run
run:
	sam local invoke --force-image-build "WidgetFunction" -e events/widget.json
	sam local invoke --force-image-build "QuoteFunction" -e events/quote.json

.PHONY: all
all: build
	sam local invoke --force-image-build "WidgetFunction" -e events/widget.json
	sam local invoke --force-image-build "QuoteFunction" -e events/quote.json


.PHONY: clean
clean:
	python setup.py clean
	git status

.PHONY: tests
tests: format lint
	pytest

