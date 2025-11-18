#!/usr/bin/env bash

set -e
set -E
set -u
set -o pipefail
set -x

function killServer() {
  pid=$(ss -lntp | awk -F 'pid=' '/:8000/ { split($2, a, ","); print a[1] }') || true
  kill "$pid" && sleep 0.5 || true
  sleep 0.5
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

# Test
killServer
bash "./start.sh" "run" "server" "--host" "127.0.0.1" "--port" "8000" "test" &
pid=$!
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
[[ "$health_check_hit" == "true" ]]
[[ "$health_check_healthy" == "true" ]]

killServer
exit 0
