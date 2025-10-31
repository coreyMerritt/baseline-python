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
bash "./scripts/install-dependencies.sh"
PYTHONPATH=src ./.venv/bin/python -m uvicorn src.main:routers --reload
