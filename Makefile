env:
	uv sync --no-dev

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

.PHONY: env install install-dev install-extras build publish format
.DEFAULT_GOAL := build
