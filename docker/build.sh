#!/usr/bin/env bash
set -e
set -E
set -o pipefail
set -u
set -x

# Args
set +u
deployment_environment="test" && [[ -n "$1" ]] && deployment_environment="$1"
docker_image_tag="test-pipelines" && [[ -n "$2" ]] && docker_image_tag="$2"
set -u

# Vars
dockerfile_path="./docker/Dockerfile"
source ".env"

# Ensure we're in the project root
while true; do
  if [[ -f "$(pwd)/pyproject.toml" ]]; then
    break
  elif [[ "$(pwd)" == "/" ]]; then
    set +x
    echo -e "\n\tFailed to find project root.\n"
    exit 1
  else
    cd ..
  fi
done

# If there's an old image with this name:tag, remove it
docker rmi "foo-project-name:${docker_image_tag}" 2>/dev/null || true

# Do the thing!
docker build \
  --no-cache \
  --build-arg "FOO_PROJECT_NAME_DEPLOYMENT_ENVIRONMENT=${deployment_environment}" \
  --build-arg "FOO_PROJECT_NAME_GLOBAL_CONFIG_DIR=${FOO_PROJECT_NAME_GLOBAL_CONFIG_DIR}" \
  --build-arg "FOO_PROJECT_NAME_MODEL_CONFIG_DIR=${FOO_PROJECT_NAME_MODEL_CONFIG_DIR}" \
  --file "$dockerfile_path" \
  --tag "foo-project-name:${docker_image_tag}" \
  "."
