#!/usr/bin/env bash

set -e
set -E
set -o pipefail
set -x

source <(curl -fsS --location "https://raw.githubusercontent.com/coreyMerritt/bash-utils/refs/heads/main/src/import")
import cdProjectRoot
import deployVenv

[[ "$1" ]] && export CHANGEME_ENVIRONMENT="$1"
cdProjectRoot
bash "./scripts/validate-environment.sh" "$CHANGEME_ENVIRONMENT" "arg1"
deployVenv
./.venv/bin/pip install --upgrade pip setuptools wheel
./.venv/bin/pip install .
if [[ "$CHANGEME_ENVIRONMENT" == "dev" ]]; then
  ./.venv/bin/pip install .[dev]
  ./.venv/bin/pre-commit install --hook-type pre-commit
  ./.venv/bin/pre-commit install --hook-type pre-push
fi
