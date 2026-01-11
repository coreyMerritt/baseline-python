#!/usr/bin/env bash
set -e
set -E
set -o pipefail
set -u
set -x

# Args
set +u
tag="test_pipelines" && [[ -n "$1" ]] && tag="$1"
database_host="172.17.0.1" && [[ -n "$2" ]] && database_host="$2"
set -u

# Vars
source "./.env"
[[ -n "$FOO_PROJECT_NAME_GLOBAL_CONFIG_DIR" ]]
[[ -n "$FOO_PROJECT_NAME_PROJECT_NAME" ]]
project_name="${FOO_PROJECT_NAME_PROJECT_NAME}"
docker_image_tag="$tag"
volume_name="${project_name}_${docker_image_tag}"
instance_name="${project_name}_${docker_image_tag}"

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

# Do the thing
docker stop $instance_name || true
docker rm $instance_name || true
docker run \
  --detach \
  --env "FOO_PROJECT_NAME_DATABASE_HOST=${database_host}" \
  --env-file ".env" \
  --name "$instance_name" \
  --publish "8080:8000" \
  --volume "${volume_name}:${FOO_PROJECT_NAME_GLOBAL_CONFIG_DIR}" \
  "$project_name:$docker_image_tag"
