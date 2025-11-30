#!/usr/bin/env bash

set -e
set -E
set -o pipefail
set -u
set -x

# Args
deployment_environment="$1"
[[ "$deployment_environment" == "test" ]] || [[ "$deployment_environment" == "dev" ]] || [[ "$deployment_environment" == "prod" ]] || {
  echo -e "\n\targ1 must be test|dev|prod\n"
  exit 1
}

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

# Point symlinks to desired environment
config_filenames_path="./src/composition/enums/config_filenames.py"
config_filenames="$(cat "$config_filenames_path" | grep -v "import" | grep -v "class" | awk '{print $3}' | jq -r)"
[[ -L "./.env" ]] || {
  [[ -f "./.env" ]] && {
    echo ".env is a regular file. Please move it to .env.d/.env.dev, .env.d/.env.prod or .env.d/.env.test"
    exit 1
  } || true
}
unlink ./.env || true
ln -s "$(pwd)/.env.d/.env.${deployment_environment}" "./.env"
[[ "$deployment_environment" == "prod" ]] && set +x
source ./.env || PROJECTNAME_GLOBAL_CONFIG_DIR="/etc/projectname"
[[ "$deployment_environment" == "prod" ]] && set -x
[[ -n "$PROJECTNAME_GLOBAL_CONFIG_DIR" ]]
for config_filename in $config_filenames; do
  unlink "${PROJECTNAME_GLOBAL_CONFIG_DIR}/${config_filename}" || true
  ln -s "${PROJECTNAME_GLOBAL_CONFIG_DIR}/${deployment_environment}/${config_filename}" "${PROJECTNAME_GLOBAL_CONFIG_DIR}/${config_filename}"
done
