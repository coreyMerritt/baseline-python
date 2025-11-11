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
bash "./start.sh" "run" "server" "--host" "127.0.0.1" "--port" "8000" "test" &
timeout=5
start_time=$(date +%s)
current_time=$(date +%s)
health_check_hit="false"
health_check_healthy="false"
while (( current_time - start_time < timeout )); do
  health_check_results="$(curl --silent --location "http://127.0.0.1:8000/api/health" | jq)" || true
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

# Get the Account
blog_post="$(curl --silent --location "http://127.0.0.1:8000/api/v1/blog?user_id=1&post_number=1" | jq)"
user_id="$(echo "$blog_post" | jq -r .user_id)"
id="$(echo "$blog_post" | jq -r .id)"
title="$(echo "$blog_post" | jq -r .title)"
body="$(echo "$blog_post" | jq -r .body)"
[[ $user_id -eq 1 ]]
[[ $id -eq 1 ]]
expected=$'sunt aut facere repellat provident occaecati excepturi optio reprehenderit'
[[ "$title" == "$expected" ]]
expected=$'quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto'
[[ "$body" == "$expected" ]]

# Cleanup
pid=$(ss -lntp | awk -F 'pid=' '/:8000/ { split($2, a, ","); print a[1] }')
kill "$pid"
sleep 1
exit 0
