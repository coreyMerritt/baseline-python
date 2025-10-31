#!/usr/bin/env bash

source <(curl -fsS --location "https://raw.githubusercontent.com/coreyMerritt/bash-utils/refs/heads/main/src/main")
cdProjectRoot
deployVenv

# Install dev dependencies
pip install --upgrade pip setuptools wheel
pip install .
pip install .[dev]
pre-commit install

# Tell user to source venv
env | grep PS1 | grep -o .venv || echo -e "\n\tsource ./.venv/bin/activate\n"
