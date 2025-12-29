#!/usr/bin/env bash
set -e
set -E
set -u
set -o pipefail
set -x

# Post the Account
response="$(
  curl \
    --silent \
    --location 'http://127.0.0.1:8000/api/v1/account' \
    --header 'Content-Type: application/json' \
    --data '{
      "name": "Test Name",
      "age": "23",
      "account_type": "business"
    }' \
      | jq  
)"
post_time=$(date +%s%3N)
error="$(echo "$response" | jq -r .error)"
[[ "$error" == "null" ]] || {
  echo -e "\n\t\"error\" is not null"
  exit 1
}
ulid="$(echo "$response" | jq -r .data.ulid)"

# Get the Account
response="$(curl --silent --location "http://127.0.0.1:8000/api/v1/account?ulid=$ulid" | jq)"
get_time=$(date +%s%3N)
error="$(echo "$response" | jq -r .error)"
[[ "$error" == "null" ]] || {
  echo -e "\n\t\"error\" is not null"
  exit 1
}
name="$(echo "$response" | jq -r .data.name)"
age=$(echo "$response" | jq -r .data.age)
account_type="$(echo "$response" | jq -r .data.account_type)"
[[ "$name" == "Test Name" ]]
[[ $age -eq 23 ]]
[[ "$account_type" == "business" ]]

# Some extra output
echo -e "\n\tDEBUG: Delay was: $(( get_time - post_time ))ms\n"

exit 0
