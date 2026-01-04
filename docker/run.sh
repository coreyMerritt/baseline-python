#!/usr/bin/env bash
set -e
set -E
set -o pipefail
set -u
set -x

# Args
set +u
tag="test-pipelines" && [[ -n "$1" ]] && tag="$1"
database_host="172.17.0.1" && [[ -n "$2" ]] && database_host="$2"
set -u

# Vars
project_name="foo-project-name"
dot_env_path="./.env"
volume_name="${project_name}-test-pipelines-volume"
project_name="foo-project-name"
dot_env_path="./.env"
docker_image_tag="${tag}"
instance_name="${project_name}-${docker_image_tag}"
volume_name="${project_name}-${tag}"

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

# Get global config dir
source "$dot_env_path"
[[ -n "$FOO_PROJECT_NAME_GLOBAL_CONFIG_DIR" ]]

# Do the thing!
docker stop $instance_name || true
docker rm $instance_name || true
docker run \
  --detach \
  --env "FOO_PROJECT_NAME_DATABASE_HOST=${database_host}" \
  --env-file "$dot_env_path" \
  --name "$instance_name" \
  --publish "8080:8000" \
  --volume "${volume_name}:${FOO_PROJECT_NAME_GLOBAL_CONFIG_DIR}" \
  "$project_name:$docker_image_tag"
