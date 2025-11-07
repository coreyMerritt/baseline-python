#!/usr/bin/env bash

set -e
set -E
set -o pipefail
set -u
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

# Vars & Validation
source .env
[[ -n "$project_environment" ]]
[[ -n "$UVICORN_HOST" ]]
[[ -n "$UVICORN_PORT" ]]
[[ -n "$PYTHONPATH" ]]
export PYTHONPATH
PROJECTNAME_ENVIRONMENT="$project_environment"  # Override env var with local var
export PROJECTNAME_ENVIRONMENT

# Start uvicorn
.venv/bin/uvicorn src.main:app \
  --host "$UVICORN_HOST" \
  --port "$UVICORN_PORT" \
  --reload \
  --reload-exclude '.venv/*' \
  --reload-exclude '*/__pycache__/*' \
  --reload-exclude '*.pyc' \
  --reload-exclude '.git'
