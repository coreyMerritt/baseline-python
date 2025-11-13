#!/usr/bin/env bash

set -e
set -E
set -o pipefail
set -u
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

.venv/bin/python ./src/main.py $@
exit 0
