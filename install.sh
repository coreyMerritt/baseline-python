#!/usr/bin/env bash

set -e
set -u
set -E
set -o pipefail
set -x

# Enforce early sudo so the script doesn't halt mid-execution
starting_user="$(id -un)"
starting_group="$(id -gn)"
sudo -k && sudo true

# Vars
config_filenames_path="src/composition/enums/config_filenames.py"
deployment_environments_path="./src/composition/enums/deployment_environment.py"
project_environment="$1"
[[ "$project_environment" == "test" ]] || [[ "$project_environment" == "dev" ]] || [[ "$project_environment" == "prod" ]] || {
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

# venv
if [[ ! -d ".venv" ]]; then
  python3 -m venv ".venv"
fi
source .venv/bin/activate

# Ensure dependencies are installed
pip install --upgrade pip setuptools wheel
if [[ "$project_environment" == "dev" ]]; then
  pip install -e .[infra,dev]
  pre-commit install
elif [[ "$project_environment" == "test" ]]; then
  pip install -e .[infra,dev]
elif [[ "$project_environment" == "prod" ]]; then
  pip install .[infra]
fi

# Configs
if [[ ! -f ".env" ]]; then
  cp -r .env.model .env
fi
source ".env"
[[ -n "$PROJECTNAME_GLOBAL_CONFIG_DIR" ]]
[[ -n "$PROJECTNAME_MODEL_CONFIG_DIR" ]]
config_filenames="$(cat "$config_filenames_path" | grep -v "import" | grep -v "class" | awk '{print $3}' | jq -r)"
deployment_environments="$(cat "$deployment_environments_path" | grep -v "import" | grep -v "class" | awk '{print $3}' | jq -r .)" 
## Assert all local configs exist
for config_filename in $config_filenames; do
  local_model_path="${PROJECTNAME_MODEL_CONFIG_DIR}/${config_filename}"
  [[ -f "$local_model_path" ]] || {
    echo -e "\n\tFatal error: $local_model_path does not exist"
    exit 1
  }
done
## Ensure all global config base dirs exist
for environment in $deployment_environments; do
  global_config_dir="${PROJECTNAME_GLOBAL_CONFIG_DIR}/${environment}"
  [[ -d "$global_config_dir" ]] || {
    sudo mkdir -p "$global_config_dir"
  }
done
sudo find "$PROJECTNAME_GLOBAL_CONFIG_DIR" -type d -exec chmod 755 {} +
## Copy any missing global configs to their respective global dir
for environment in $deployment_environments; do
  for config_filename in $config_filenames; do
    local_model_path="${PROJECTNAME_MODEL_CONFIG_DIR}/${config_filename}"
    global_config_path="${PROJECTNAME_GLOBAL_CONFIG_DIR}/${environment}/${config_filename}"
    [[ -f "$global_config_path" ]] || {
      sudo cp -r "$local_model_path" "$global_config_path"
    }
  done
done
sudo chown -R "$starting_user:$starting_group" "$PROJECTNAME_GLOBAL_CONFIG_DIR"
sudo find "$PROJECTNAME_GLOBAL_CONFIG_DIR" -type f -exec chmod 644 {} +

# If is prod install, make binary and toss into /usr/bin
project_name_as_bin="projectname"
installation_dir="/usr/bin"
installation_path="${installation_dir}/${project_name_as_bin}"
if [[ "$project_environment" == "prod" ]]; then
  ./.venv/bin/pyinstaller \
    --onefile \
    --hidden-import=interfaces.rest.webserver_hook \
    --name=${project_name_as_bin} \
    src/interfaces/command_line/entrypoint.py
  sudo cp "./dist/${project_name_as_bin}" "$installation_path"
  sudo chmod 755 "$installation_path"
fi
exit 0
