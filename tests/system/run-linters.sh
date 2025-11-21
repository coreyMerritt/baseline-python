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
PYTHONPATH=./tests/ ./tests/linters/abstract_classes_have_an_abstract_method.py
PYTHONPATH=./tests/ ./tests/linters/classes_are_implemented.py
PYTHONPATH=./tests/ ./tests/linters/classes_are_imported.py
PYTHONPATH=./tests/ ./tests/linters/errs_dont_inherit_directly_from_exception.py
./tests/linters/imports-flow-in-correct-direction.sh
PYTHONPATH=./tests/ ./tests/linters/methods_declare_return_type.py
PYTHONPATH=./tests/ ./tests/linters/methods_have_low_arg_count.py
PYTHONPATH=./tests/ ./tests/linters/service_exceptions_are_imported_in_interfaces.py
.venv/bin/python -m isort --check-only .
.venv/bin/python -m mypy .
.venv/bin/python -m pylint ./scripts/
.venv/bin/python -m pylint ./src/
.venv/bin/python -m pylint ./tests/
.venv/bin/python -m ruff check .
exit 0
