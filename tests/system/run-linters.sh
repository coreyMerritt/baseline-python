#!/usr/bin/env bash

set -e
set -u
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

# Validate some binaries
which .venv/bin/pip
which .venv/bin/python

# Validate some packages
.venv/bin/pip show isort 1>/dev/null
.venv/bin/pip show mypy 1>/dev/null
.venv/bin/pip show pylint 1>/dev/null
.venv/bin/pip show ruff 1>/dev/null

# Test
./tests/linters/third-party-linters.sh
./tests/linters/import-flow-check.sh
PYTHONPATH=./tests/ ./tests/linters/direct_exception_inheritence_check.py
PYTHONPATH=./tests/ ./tests/linters/unimplemented_classes_check.py
PYTHONPATH=./tests/ ./tests/linters/unimported_classes_check.py
exit 0
