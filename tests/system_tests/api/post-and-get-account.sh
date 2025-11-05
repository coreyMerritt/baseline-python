#!/usr/bin/env bash

sudo true
source <(curl -fsS --location "https://raw.githubusercontent.com/coreyMerritt/bash-utils/refs/heads/main/src/main")
import "bash-test" $@

btInfo "Setting up test environment..."
  cdProjectRoot
  deployVenv
  source .venv/bin/activate
  pip install --upgrade pip setuptools wheel
  pip install .
  [[ -d "./config/test/" ]] || mkdir "./config/test/"
  cp -r ./config/model/* "./config/test/"
  bash "./scripts/deploy-db.sh" "test" "true"
  bash "./start-with-uvicorn.sh" "test" &

timeout=60
start_time=$(date +%s)
current_time=$(date +%s)
btInfo "Waiting for system to start..."
  while (( current_time - start_time < 60 )); do
    health_check_results="$(curl --location "http://127.0.0.1:8000/api/health/")" || true
    healthy="$(echo "$health_check_results" | jq .healthy)" || true
    if [[ "$healthy" == "true" || "$healthy" == "True" ]]; then
      break
    fi
    sleep 1
    current_time=$(date +%s)
  done

btStartTest "Post Account"
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

btStartTest "Get Account"
  account="$(curl --location "http://127.0.0.1:8000/api/v1/account?uuid=$uuid")"
  get_time=$(date +%s%3N)
  name="$(echo "$account" | jq -r .name)"
  age=$(echo "$account" | jq -r .age)
  account_type="$(echo "$account" | jq -r .account_type)"
  [[ "$name" == "Test Name" ]]
  [[ $age -eq 23 ]]
  [[ "$account_type" == "business" ]]

btInfo "Delay was: $(( get_time - post_time ))ms"

# Cleanup
pkill -f uvicorn
sleep 1
