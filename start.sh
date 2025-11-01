#!/usr/bin/env bash

set -e
set -E
set -o pipefail
set -x

source <(curl -fsS --location "https://raw.githubusercontent.com/coreyMerritt/bash-utils/refs/heads/main/src/import")
import cdProjectRoot
import deployVenv

[[ "$1" ]] && export PROJECTNAME_ENVIRONMENT="$1"
cdProjectRoot
bash "./scripts/validate-environment.sh" "$PROJECTNAME_ENVIRONMENT" "arg1"
deployVenv
./.venv/bin/pip install --upgrade pip setuptools wheel
./.venv/bin/pip install .
if [[ "$PROJECTNAME_ENVIRONMENT" == "dev" ]]; then
  ./.venv/bin/pip install .[dev]
  pre-commit install
fi
python3 ./src/main.py $@
