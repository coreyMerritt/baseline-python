#!/usr/bin/env bash
set -e
set -E
set -o pipefail
set -u
set -x

# Vars
project_name="projectname"
docker_compose_env_path="./.env.docker-compose"
new_password="$(openssl rand -hex 32)"
PROJECTNAME_DATABASE_PASSWORD=$new_password

# docker-compose will need these for parse-time vars
source "$docker_compose_env_path"
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

# Bring everything down before we starting messing with things
docker compose down || true

# Replace PROJECTNAME_DATABASE_PASSWORD
to_replace="$(cat .env.docker-compose | grep -E "[.+]?PROJECTNAME_DATABASE_PASSWORD.+")"
replacement="PROJECTNAME_DATABASE_PASSWORD=${new_password}"
sed -i "s/$to_replace/$replacement/g" "$docker_compose_env_path"
# Replace POSTGRES_PASSWORD
to_replace="$(cat .env.docker-compose | grep -E "[.+]?POSTGRES_PASSWORD.+")"
replacement="POSTGRES_PASSWORD=${new_password}"
sed -i "s/$to_replace/$replacement/g" "$docker_compose_env_path"
# Ensure we're not trying to remount a used volume
volume_yq_paths=(
  ".volumes.postgres-18-volume.name"
  ".volumes.projectname-configs-volume.name"
)
for volume_yq_path in ${volume_yq_paths[@]}; do
  volume_name="$(cat docker-compose.yml | yq "$volume_yq_path")"
  if docker volume list | grep -o "$volume_name"; then
    echo -e "\n\tVolume already exists: $volume_name"
    echo -e "\tRemove the volume and run again:"
    echo -e "\t\tdocker volume rm $volume_name"
    exit 1
  fi
done

docker compose up --detach
