#!/usr/bin/env bash
set -e
set -E
set -u
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
.venv/bin/pip show pytest

# Test
echo -e "\n\tRunning unit tests...\n"
.venv/bin/python3 -m pytest -v ./tests/unit
exit 0
