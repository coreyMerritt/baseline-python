#!/usr/bin/env bash

source <(curl -fsS --location "https://raw.githubusercontent.com/coreyMerritt/bash-utils/refs/heads/main/src/main")
import "bash-test" $@

btInfo "Setting up environment..."
  cdProjectRoot
  deployVenv
  bash "./scripts/install-dependencies.sh" "dev"

btStartTest "isort passes"
  .venv/bin/python -m isort --check-only ./src/

btStartTest "mypy passes"
  .venv/bin/python -m mypy ./src/

btStartTest "pylint passes"
  .venv/bin/python -m pylint --disable=fixme ./src/

btStartTest "ruff passes"
  .venv/bin/python -m ruff check ./src/
