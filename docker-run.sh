#!/usr/bin/env bash

set -e
set -E
set -o pipefail
set -u
set -x

# Args
deployment_environment="$1"
instance_name="$2"
set +u
database_host="172.17.0.1" && [[ -n "$3" ]] && database_host="$3"
set -u

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

# Vars
project_name="projectname"
image_tag="test-pipelines-image"
dot_env_path="./.env"
volume_name="${project_name}-test-pipelines-volume"

source "$dot_env_path"
[[ -n "$PROJECTNAME_GLOBAL_CONFIG_DIR" ]]



docker stop $instance_name || true
docker rm $instance_name || true
docker run \
  --detach \
  --env "PROJECTNAME_DATABASE_HOST=${database_host}" \
  --env-file "$dot_env_path" \
  --name "$instance_name" \
  --publish "8080:8000" \
  --volume "${volume_name}:${PROJECTNAME_GLOBAL_CONFIG_DIR}" \
  "$project_name:$image_tag" \
  "$deployment_environment"
