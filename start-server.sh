#!/usr/bin/env bash

set -e
set -E
set -o pipefail
set -u
set -x

# Validate args
set +u
deployment_environment="$1"
[[ -n "$deployment_environment" ]] || {
  deployment_environment="$PROJECTNAME_DEPLOYMENT_ENVIRONMENT"
}
set -u
[[ "$deployment_environment" == "dev" ]] || {
  [[ "$deployment_environment" == "prod" ]] || {
    [[ "$deployment_environment" == "test" ]] || {
      echo -e "\n\tUnknown deployment environment\n"
      exit 1
    }
  }
}

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

# Load environment
./scripts/set-deployment-environment.sh "$deployment_environment"
[[ "$deployment_environment" == "prod" ]] && set +x
set -a
source ./.env
set +a
[[ "$deployment_environment" == "prod" ]] && set -x

# Run server
.venv/bin/python -u ./src/composition/cli_entrypoint.py
exit 0
