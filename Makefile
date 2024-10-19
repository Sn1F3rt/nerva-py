env:
	uv sync --no-dev

dev:
	uv sync --all-extras

format:
	ruff check --select I --fix .
	ruff format .

build:
	uv build

publish:
	uv publish --token $(token)

.PHONY: env dev format build publish
.DEFAULT_GOAL := build
