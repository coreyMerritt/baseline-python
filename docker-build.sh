#!/usr/bin/env bash

set -e
set -E
set -o pipefail
set -u
set -x

deployment_environment="$1"
tag="$2"

source ".env"

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

# Copy our actual configs over
cp -r "$PROJECTNAME_GLOBAL_CONFIG_DIR/test" "./config/" 

docker rmi "projectname:${tag}" || true
docker build \
  --no-cache \
  --build-arg "PROJECTNAME_DEPLOYMENT_ENVIRONMENT=${deployment_environment}" \
  --build-arg "PROJECTNAME_GLOBAL_CONFIG_DIR=${PROJECTNAME_GLOBAL_CONFIG_DIR}" \
  --build-arg "PROJECTNAME_MODEL_CONFIG_DIR=${PROJECTNAME_MODEL_CONFIG_DIR}" \
  --file "Dockerfile" \
  --tag "projectname:${tag}" \
  "."
