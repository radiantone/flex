.DEFAULT_GOAL := all
black = black --target-version py39 flex
isort = isort --profile black flex

.PHONY: depends
depends:
	@echo "Installing OS dependencies..."
	@bash ./bin/depends.sh
	@echo "Done"

.PHONY: init
init: depends
	@echo "Setting up virtual environment in venv/"
	@python3 -m venv venv
	@echo "Virtual environment complete."


.PHONY: format
format:
	$(isort)
	$(black)

.PHONY: lint
lint: setup-install
	mypy --show-error-codes  --ignore-missing-imports flex
	flake8 --ignore=E203,F841,E501,E722,W503  flex
	$(isort) --check-only --df
	$(black) --check --diff

.PHONY: setup-install
setup-install:
	python setup.py install

.PHONY: install
install: depends init
	. venv/bin/activate && ( \
	pip install -r requirements.txt ; \
	python setup.py install ; \
	python setup.py clean \
	)


.PHONY: update
update: format lint
	pip freeze | grep -v flex > requirements.txt
	git add setup.py docs bin flex requirements.txt Makefile
	git commit --allow-empty -m "Updates"
	git push origin main
	python setup.py install
	git status

.PHONY: docs
docs:
	cd docs
	make -C docs html

.PHONY: clean
clean:
	python setup.py clean
	git status

.PHONY: tests
tests: format lint
	pytest
	
.PHONY: all
all: format lint update docs install tests clean
	git status
