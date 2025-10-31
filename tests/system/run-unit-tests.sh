#!/usr/bin/env bash

source <(curl -fsS --location "https://raw.githubusercontent.com/coreyMerritt/bash-utils/refs/heads/main/src/main")

cdProjectRoot
deployVenv
bash "./scripts/install-dependencies.sh" "dev"
.venv/bin/python -m pytest -v
