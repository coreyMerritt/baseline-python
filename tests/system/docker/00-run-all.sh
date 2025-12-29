#!/usr/bin/env bash
set -e
set -E
set -u
set -o pipefail
set -x

# Vars
deployment_environment="test"
project_name="projectname"
docker_image_tag="test-pipelines"
instance_name="${project_name}-${docker_image_tag}"
volume_name="${project_name}-${docker_image_tag}"

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
source "./tests/system/docker/_helpers.sh"

# Ensure test resources exist
fullCleanup
set +u
if ! docker images --format "{{.Repository}}:{{.Tag}}" | grep "$project_name" | grep "$docker_image_tag"; then
  ./docker/build.sh "test" "$docker_image_tag"
fi
set -u

# Test
bash "./tests/system/docker/image-runs.sh"
softCleanup
bash "./tests/system/docker/docker-compose-runs.sh"

# Cleanup
fullCleanup
exit 0
