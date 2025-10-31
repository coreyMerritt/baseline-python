#!/usr/bin/env bash

set -e
set -E
set -o pipefail
set -x

source <(curl -fsS --location "https://raw.githubusercontent.com/coreyMerritt/bash-utils/refs/heads/main/src/import")
import cdProjectRoot
import dockerDeployPostgres

cdProjectRoot
[[ "$1" ]] && export CHANGEME_ENVIRONMENT="$1"
bash "./scripts/validate-environment.sh" "$1" "arg1"
db_config_path="./config/$1/database.yml"
postgres_user="$(uuidgen | cut -c1-8)"
postgres_password="$(uuidgen | cut -c1-8)"
postgres_name="CHANGEME-$1"
[[ "$1" == "test" ]] && postgres_port=5435  || true   # Avoid collision with potential real dbs on the host
[[ "$1" == "dev" ]] && postgres_port=5435 || true   # Avoid collision with potential real dbs on the host
[[ "$1" == "prod" ]] && postgres_port=5432 || true
container_name="postgres-$1"
container_version="17"
cat << EOF > "$db_config_path"
engine: "postgresql"
username: "$postgres_user"
password: "$postgres_password"
host: "127.0.0.1"
port: $postgres_port
name: "$postgres_name"
EOF
dockerDeployPostgres \
  "$postgres_user" \
  "$postgres_password" \
  "$postgres_name" \
  "$postgres_port" \
  "$container_name" \
  "$container_version"
