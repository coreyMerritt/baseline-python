#!/usr/bin/env bash

set -e
set -u
set -E
set -o pipefail
set -x

# Vars
project_environment="$1"
[[ "$project_environment" == "test" ]] || [[ "$project_environment" == "dev" ]] || [[ "$project_environment" == "prod" ]] || {
  echo -e "\n\targ1 must be test|dev|prod\n"
  exit 1
}

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

# venv
if [[ ! -d ".venv" ]]; then
  python3 -m venv ".venv"
fi
source .venv/bin/activate

# Ensure dependencies are installed
pip install --upgrade pip setuptools wheel
pip install -e .[infra]
if [[ "$project_environment" == "dev" ]]; then
  pip install -e .
  pip install -e .[dev]
  pre-commit install
elif [[ "$project_environment" == "test" ]]; then
  pip install -e .
elif [[ "$project_environment" == "prod" ]]; then
  pip install .
fi

# Ensure basic non-sensitive configs are in place
if [[ ! -d "./config/${project_environment}/logging.yml" ]]; then
  cp -r "./config/model/logging.yml" "./config/${project_environment}/logging.yml"
fi
