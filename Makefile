PORT ?= 8080
URL_BASE_PATHNAME ?= /

install:
	poetry install
	poetry run pre-commit install

flake8:
	git ls-files '*.py' | flake8 --count

pylint:
	git ls-files '*.py' | xargs pylint --disable=duplicate-code --fail-under=10

black:
	git ls-files '*.py' | black --check .

pytest:
	@echo recipe not implemented
	# TODO: Enable tests
	# poetry run pytest --no-cov-on-fail --cov-fail-under=70 --cov-branch --cov-report=term --cov-report=html:htmlcov --cov=src

export_requirements:
	poetry export -f requirements.txt --without-hashes -o requirements/prod.txt
	poetry export --only dev -f requirements.txt --without-hashes -o requirements/dev.txt
