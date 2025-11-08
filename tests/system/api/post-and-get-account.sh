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

# venv
if [[ ! -d ".venv" ]]; then
  python3 -m venv ".venv"
fi
source .venv/bin/activate

# Wait for system to start
bash "./start.sh" "test" &
timeout=60
start_time=$(date +%s)
current_time=$(date +%s)
health_check_hit="false"
health_check_healthy="false"
while (( current_time - start_time < 60 )); do
  health_check_results="$(curl --location "http://127.0.0.1:8000/api/health/")" || true
  healthy="$(echo "$health_check_results" | jq .healthy)" || true
  if [[ "$health_check_hit" == "false" && -n "$healthy" ]]; then
    health_check_hit="true"
  fi
  if [[ "$healthy" == "true" || "$healthy" == "True" ]]; then
    health_check_healthy="true"
    break
  fi
  sleep 1
  current_time=$(date +%s)
done
[[ "$health_check_hit" == "true" ]]
[[ "$health_check_healthy" == "true" ]]

# Post the Account
  result="$(
    curl \
      --location 'http://127.0.0.1:8000/api/v1/account' \
      --header 'Content-Type: application/json' \
      --data '{
        "name": "Test Name",
        "age": "23",
        "account_type": "business"
      }'
  )"
  post_time=$(date +%s%3N)
  status="$(echo "$result" | jq -r .status)"
  uuid="$(echo "$result" | jq -r .uuid)"
  [[ "$status" == "Success" ]]

# Get the Account
  account="$(curl --location "http://127.0.0.1:8000/api/v1/account?uuid=$uuid")"
  get_time=$(date +%s%3N)
  name="$(echo "$account" | jq -r .name)"
  age=$(echo "$account" | jq -r .age)
  account_type="$(echo "$account" | jq -r .account_type)"
  [[ "$name" == "Test Name" ]]
  [[ $age -eq 23 ]]
  [[ "$account_type" == "business" ]]

# Some extra output
echo -e "\n\tDEBUG: Delay was: $(( get_time - post_time ))ms\n"

# Cleanup
pkill -f uvicorn
sleep 1
