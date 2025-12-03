#!/usr/bin/env bash
set -e
set -E
set -o pipefail
set -u
set -x

# Args
deployment_environment="$1"
docker_tag="$2"
[[ "$1" == "dev" || "$1" == "prod" || "$1" == "test" ]]

# Vars
project_name="projectname"
docker_env_path="./.env"
new_password="$(openssl rand -hex 32)"
PROJECTNAME_DATABASE_PASSWORD=$new_password

# Functions
function safeSed() {
  to_replace="$1"
  replacement="$2"
  docker_env_path="$3"
  tmp=$(mktemp)
  sed "s/$to_replace/$replacement/g" "$docker_env_path" > "$tmp"
  cat "$tmp" > "$docker_env_path"   # writes through the symlink, a direct write would break symlinks
  rm "$tmp"
}

# docker-compose will need these for parse-time vars
source "$docker_env_path"
export POSTGRES_DB
export POSTGRES_USER
export COMPOSE_PROJECT_NAME

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

# Package Check
if ! which yq; then
  echo -e "\n\Install yq and run again.\n"; exit 1
fi

# Ensure everything is down before we starting messing with things
DOCKER_TAG="silences-a-silly-warning" docker compose down || true

# Replace PROJECTNAME_DATABASE_PASSWORD
to_replace="$(cat "$docker_env_path" | grep -E "[.+]?PROJECTNAME_DATABASE_PASSWORD.+")"
replacement="PROJECTNAME_DATABASE_PASSWORD=${new_password}"
safeSed "$to_replace" "$replacement" "$docker_env_path"
# Replace POSTGRES_PASSWORD
to_replace="$(cat "$docker_env_path" | grep -E "[.+]?POSTGRES_PASSWORD.+")"
replacement="POSTGRES_PASSWORD=${new_password}"
safeSed "$to_replace" "$replacement" "$docker_env_path"
# Ensure we're not trying to remount a used volume
volume_yq_paths=(
  ".volumes.postgres-18-volume.name"
  ".volumes.${project_name}-configs-volume.name"
)
for volume_yq_path in ${volume_yq_paths[@]}; do
  volume_name="$(cat docker-compose.yml | yq "$volume_yq_path")"
  if docker volume list | grep -o "$volume_name"; then
    if [[ ! "$volume_name" =~ "test" ]] && [[ ! "$volume_name" =~ "dev" ]]; then
      echo -e "\n\tVolume already exists: $volume_name"
      echo -e "\tRemove the volume and run again:"
      echo -e "\t\tdocker volume rm $volume_name"
      exit 1
    else
      docker volume rm "$volume_name"
    fi
  fi
done

# Ensure image exists, if not build it
set +u
image_exists="$(docker image list | grep "$project_name" | awk '{print $2}' | grep -E "^${docker_tag}$" || true)"
if [[ ! -n "$image_exists" ]]; then
  ./docker-build.sh "$deployment_environment" "$docker_tag"
fi
set -u

# Do the thing!
./scripts/set-deployment-environment.sh "$deployment_environment"
DOCKER_TAG="$docker_tag" docker compose up --detach
