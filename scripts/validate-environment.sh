#!/usr/bin/env bash

set -e
set -E
set -o pipefail
set -x

source <(curl -fsS --location "https://raw.githubusercontent.com/coreyMerritt/bash-utils/refs/heads/main/src/error")

env="$1"
[[ "$2" ]] && parameter="$2" || parameter="arg1"

[[ "$env" == "test" ]] || [[ "$env" == "dev" ]] || [[ "$env" == "prod" ]] || error "\n\tMust pass $parameter test|dev|prod\n"
