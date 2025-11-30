#!/usr/bin/env bash

set -e
set -E
set -o pipefail
set -u
set -x

tag="$1"

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

docker rmi "projectname:${tag}" || true
docker build \
  --no-cache \
  --file "Dockerfile" \
  --tag "projectname:${tag}" \
  "."
