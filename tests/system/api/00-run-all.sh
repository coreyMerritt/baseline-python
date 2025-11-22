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

# Test
bash "./tests/system/api/health-check.sh"
bash "./tests/system/api/get-blog-post.sh"
bash "./tests/system/api/post-and-get-account.sh"
exit 0
