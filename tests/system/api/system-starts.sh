#!/usr/bin/env bash

sudo true
source <(curl -fsS --location "https://raw.githubusercontent.com/coreyMerritt/bash-utils/refs/heads/main/src/main")
import "bash-test" $@

btInfo "Setting up test environment..."
  cdProjectRoot
  deployVenv
  source .venv/bin/activate
  pip install --upgrade pip setuptools wheel
  pip install .
  [[ -d "./config/test/" ]] || mkdir "./config/test/"
  cp -r ./config/model/* "./config/test/"
  bash "./scripts/deploy-db.sh" "test" "true"

btStartTest "Dry run with no webserver does not throw"
  PROJECTNAME_ENVIRONMENT="test" python3 ./src/main.py $@
