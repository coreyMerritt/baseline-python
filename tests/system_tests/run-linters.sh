#!/usr/bin/env bash
set -e
set -E
set -o pipefail
set -x

# Ensure we're in the project root
while true; do
  if [[ -f "$(pwd)/pyproject.toml" ]]; then
    break
  elif [[ "$(pwd)" == "/" ]]; then
    echo -e "\n\tFailed to find project root.\n"; exit 1
  else
    cd ..
  fi
done

# Deploy venv if not already deployed
if [[ ! -d ".venv" ]]; then
  python3 -m venv ".venv"
fi

# Install dev dependencies if not already installed
.venv/bin/pip install .[dev]

# Test
echo -e "\n\tStarting linting/formating tests...\n"
.venv/bin/python -m isort --check-only ./src/
.venv/bin/python -m mypy ./src/
.venv/bin/python -m pylint --disable=fixme ./src/
.venv/bin/python -m ruff check ./src/
