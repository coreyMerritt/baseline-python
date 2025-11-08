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

# venv
if [[ ! -d ".venv" ]]; then
  python3 -m venv ".venv"
fi
source .venv/bin/activate

# Test
timeout=30
start_time=$(date +%s)
current_time=$(date +%s)
success="false"
while (( current_time - start_time < 60 )); do
  set +e
  PROJECTNAME_ENVIRONMENT="test" .venv/bin/python3 ./src/main.py
  rc=$?
  set -e
  if [[ $rc -eq 0 ]]; then
    success="true"
    break
  fi
  sleep 1
  current_time=$(date +%s)
done
[[ "$success" == "true" ]]
