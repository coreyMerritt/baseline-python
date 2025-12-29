#!/usr/bin/env bash
set -e
set -E
set -o pipefail
set -u
set -x

# Args
set +u
docker_image_tag="test-pipelines" && [[ -n "$1" ]] && docker_image_tag="$1"
set -u

# Vars
project_name="projectname"
docker_env_path="./.env"
docker_compose_path="./docker/docker-compose.yml"

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
    set +x
    echo -e "\n\tFailed to find project root.\n"
    exit 1
  else
    cd ..
  fi
done

# Package Check
if ! which yq; then
  set +x
  echo -e "\n\Install yq and run again.\n"
  exit 1
fi

# Ensure everything is down before we starting messing with things
DOCKER_TAG="silences-a-silly-warning" docker compose down || true

is_password="$(cat "$docker_env_path" | grep -oE "PROJECTNAME_DATABASE_PASSWORD=.+")"
if [[ ! -n "$is_password" ]]; then
  new_password="$(openssl rand -hex 32)"
  POSTGRES_PASSWORD="$new_password"
  PROJECTNAME_DATABASE_PASSWORD="$new_password"
  # Replace PROJECTNAME_DATABASE_PASSWORD
  to_replace="$(cat "$docker_env_path" | grep -E "[.+]?PROJECTNAME_DATABASE_PASSWORD.+")"
  replacement="PROJECTNAME_DATABASE_PASSWORD=${new_password}"
  safeSed "$to_replace" "$replacement" "$docker_env_path"
  # Replace POSTGRES_PASSWORD
  to_replace="$(cat "$docker_env_path" | grep -E "[.+]?POSTGRES_PASSWORD.+")"
  replacement="POSTGRES_PASSWORD=${new_password}"
  safeSed "$to_replace" "$replacement" "$docker_env_path"
fi
# Ensure we're not trying to remount a used volume
docker_compose_path="./docker/docker-compose.yml"
volume_yq_paths=(
  ".volumes.postgres-18-volume.name"
  ".volumes.${project_name}-configs-volume.name"
)
for volume_yq_path in ${volume_yq_paths[@]}; do
  volume_name="$(cat "$docker_compose_path" | yq "$volume_yq_path")"
  if docker volume list | grep -o "$volume_name"; then
    set +x
    echo -e "\n\tVolume already exists: $volume_name"
    echo -e "\tIf credentials issues exist, consider removing the volume with:"
    echo -e "\t\tdocker volume rm $volume_name"
    set -x
  fi
done

# Do the thing
docker_image_tag="$docker_image_tag" docker compose \
  --env-file "$(cd "$(dirname "$0")/.." && pwd)/.env" \
  --file "$docker_compose_path" \
  up \
  --detach
