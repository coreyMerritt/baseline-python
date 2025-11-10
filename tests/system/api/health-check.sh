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

# Test
bash "./start.sh" "run" "server" "--host" "127.0.0.1" "--port" "8000" "test" &
pid=$!
timeout=5
start_time=$(date +%s)
current_time=$(date +%s)
health_check_hit="false"
health_check_healthy="false"
while (( current_time - start_time < timeout )); do
  health_check_results="$(curl --silent --location "http://127.0.0.1:8000/api/health/" | jq)" || true
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

# Cleanup
pid=$(ss -lntp | awk -F 'pid=' '/:8000/ { split($2, a, ","); print a[1] }')
kill "$pid"
sleep 1
exit 0
