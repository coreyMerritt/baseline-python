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

bash "./start.sh" "test" &

timeout=60
start_time=$(date +%s)
current_time=$(date +%s)
while (( current_time - start_time < 60 )); do
  health_check_results="$(curl --location "http://127.0.0.1:8000/api/health/")" || true
  healthy="$(echo "$health_check_results" | jq .healthy)" || true
  if [[ "$healthy" == "true" || "$healthy" == "True" ]]; then
    break
  fi
  sleep 1
  current_time=$(date +%s)
done

# Cleanup
pkill -f uvicorn
sleep 1
