#!/usr/bin/env bash

source <(curl -fsS --location "https://raw.githubusercontent.com/coreyMerritt/bash-utils/refs/heads/main/src/main")
import "bash-test" $@

cdProjectRoot
deployVenv
bash "./scripts/install-dependencies.sh" "dev"

btStartTest "pytest passes"
  .venv/bin/python -m pytest -v
