#!/usr/bin/env bash

set -e
set -E
set -u
set -o pipefail
set -x

# Get the Account
response="$(curl --silent --location "http://127.0.0.1:8000/api/v1/blog?user_ulid=1&post_number=1" | jq)"
error="$(echo "$response" | jq -r .error)"
[[ "$error" == "null" ]] || {
  echo -e "\n\t\"error\" is not null"
  exit 1
}
user_ulid="$(echo "$response" | jq -r .data.user_ulid)"
id="$(echo "$response" | jq -r .data.id)"
title="$(echo "$response" | jq -r .data.title)"
body="$(echo "$response" | jq -r .data.body)"
[[ $user_ulid -eq 1 ]] || {
  echo -e "\n\tUnexpected result: user_ulid"
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

exit 0
