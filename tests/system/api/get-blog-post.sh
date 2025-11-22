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
source "./tests/system/api/_helper.sh"

# venv
if [[ ! -d ".venv" ]]; then
  python3 -m venv ".venv"
fi
source ".venv/bin/activate"

# Wait for system to start
startServer
timeout=5
start_time=$(date +%s)
current_time=$(date +%s)
health_check_hit="false"
health_check_healthy="false"
while (( current_time - start_time < timeout )); do
  health_check_results="$(curl --silent --location "http://127.0.0.1:8000/api/health" | jq)" || true
  healthy="$(echo "$health_check_results" | jq .data.healthy)" || true
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
[[ "$health_check_hit" == "true" ]] || {
  echo -e "\n\tFailed to hit health endpoint"
  exit 1
}
[[ "$health_check_healthy" == "true" ]] || {
  echo -e "\n\tHealth endpoint did not return healthy"
  exit 1
}

# Get the Account
response="$(curl --silent --location "http://127.0.0.1:8000/api/v1/blog?user_id=1&post_number=1" | jq)"
error="$(echo "$response" | jq -r .error)"
[[ "$error" == "null" ]] || {
  echo -e "\n\t\"error\" is not null"
  exit 1
}
user_id="$(echo "$response" | jq -r .data.user_id)"
id="$(echo "$response" | jq -r .data.id)"
title="$(echo "$response" | jq -r .data.title)"
body="$(echo "$response" | jq -r .data.body)"
[[ $user_id -eq 1 ]] || {
  echo -e "\n\tUnexpected result: user_id"
  exit 1
}
[[ $id -eq 1 ]] || {
  echo -e "\n\tUnexpected result: id"
  exit 1
}
expected=$'sunt aut facere repellat provident occaecati excepturi optio reprehenderit'
[[ "$title" == "$expected" ]] || {
  echo -e "\n\tUnexpected result: title"
  exit 1
}
expected=$'quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto'
[[ "$body" == "$expected" ]] || {
  echo -e "\n\tUnexpected result: body"
  exit 1
}

cleanup
exit 0
