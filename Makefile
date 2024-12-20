env:
	uv venv

rmenv:
	rm -rf .venv

install:
	uv sync --no-dev

install-dev:
	uv sync --extra dev

build:
	uv build

publish:
	uv publish --token $(token)

format:
	ruff check --select I --fix .
	ruff format .

.PHONY: env rmenv install install-dev build publish format
.DEFAULT_GOAL := build
