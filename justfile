#!/usr/bin/env -S just --justfile

alias s := style
alias l := lint
alias c := check
alias f := format
alias d := dev
alias ie := i18n-extract
alias iu := i18n-update
alias ic := i18n-compile

[doc("List available recipes")]
[private]
default:
    just --list --unsorted

[doc("Initialize development environment")]
init:
    uv run --locked --group dev pre-commit install

[doc("Run style recipes on source files")]
[group("style")]
style: lint check format

[doc("Run mypy on source files")]
[group("style")]
lint:
    uv run --locked --group style mypy

[doc("Run Ruff on source files")]
[group("style")]
check:
    uv run --locked --group style ruff check --fix

[doc("Run Ruff formatter on source files")]
[group("style")]
format:
    uv run --locked --group style ruff format

[doc("Start development server")]
[group("dev")]
dev: i18n-compile
    uv run --locked --module src

[doc("Build production binary file")]
[group("build")]
build:
    uv run --locked --group build pyinstaller --onefile --hidden-import=greenlet --hidden-import=aiosqlite ./src/__main__.py

[doc("Apply pending SQLite migrations")]
[group("sqlite")]
sqlite-migrate:
    uv run --locked alembic --name sqlite upgrade head

[group("i18n")]
i18n-extract:
    uv run --locked pybabel extract -w 120 -k _:1,1t -k _:1,2 -k __ --input-dirs=. -o locales/messages.pot

[group("i18n")]
i18n-update:
    uv run --locked pybabel update -w 120 -d locales -D messages -i locales/messages.pot

[group("i18n")]
i18n-compile:
    uv run --locked pybabel compile -d locales -D messages --statistics

[unix]
[doc("Clean build artifacts and cache directories")]
[group("clean")]
[confirm("Do you really want to clean build artifacts and cache directories (y/N)?")]
clean:
    find . -type d -name __pycache__ -exec rm -rf {} +
    rm -rf .cache .mypy_cache .pytest_cache .ruff_cache .venv *.spec *.egg-info .coverage build dist site coverage.lcov
