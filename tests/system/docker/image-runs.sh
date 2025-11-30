#!/usr/bin/env bash

set -e
set -E
set -u
set -o pipefail
set -x

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
deployment_environment="test"
project_name="projectname"
image_tag="test-pipelines-image"
dot_env_path="./.env"
instance_name="${project_name}-test-pipelines-instance"
volume_name="${project_name}-test-pipelines-volume"


# Set environment
./scripts/set-deployment-environment.sh "$deployment_environment"

# Env Vars
source "$dot_env_path"
[[ -n "$PROJECTNAME_GLOBAL_CONFIG_DIR" ]]

# Remove old running test instances
if docker ps | grep "$instance_name"; then
  docker stop "$instance_name"
fi
if docker ps -a | grep "$instance_name"; then
  docker rm "$instance_name"
fi
# Build the image if it isn't already built
if ! docker image list | grep "$project_name" | grep "$image_tag"; then
  ./docker-build.sh "$deployment_environment" "$image_tag"
fi
# Remove the volume if it exists
if docker volume list | grep "$volume_name"; then
  docker volume rm "$volume_name"
fi

# Test
./docker-run.sh "$deployment_environment" "$instance_name"
timeout=30
container_is_healthy=0
didnt_time_out=0
start_time=$(date +%s)
while (( $(date +%s) - start_time < timeout )); do
  if res="$(docker exec -it "$instance_name" curl --silent http://localhost:8000/api/health/full | jq)"; then
    healthy="$(echo "$res" | jq .data.healthy)"
    if [[ "$healthy" == "true" ]]; then
      didnt_time_out=1
      container_is_healthy=1
      break
    fi
  fi
  sleep 1
done
(( didnt_time_out ))
(( container_is_healthy ))

# If everything succeeded: Cleanup
if docker ps | grep "$instance_name"; then
  docker stop "$instance_name"
fi
if docker ps -a | grep "$instance_name"; then
  docker rm "$instance_name"
fi
# if docker image list | grep "$project_name" | grep "$image_tag"; then
#   docker rmi "${project_name}:${image_tag}"
# fi
# if docker volume list | grep "$volume_name"; then
#   docker volume rm "$volume_name"
# fi

exit 0
