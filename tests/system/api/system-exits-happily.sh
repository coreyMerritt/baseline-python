#!/usr/bin/env bash
# NOTE: Although unintuitive, this is intentionally marked as an "api" test as it demands being run with a webserver

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
source "./tests/system/api/_helpers.sh"

# venv
if [[ ! -d ".venv" ]]; then
  python3 -m venv ".venv"
fi
source ".venv/bin/activate"

# Test
log_path="/tmp/projectname-exit-test.log"
startServer
sleep 5
killServer
cat "$log_path" | grep -o "Traceback" && rc=$? || rc=$?
[[ $rc -eq 1 ]] || { 
  echo -e "\n\tSystem shutdown logs contain a traceback"
  exit 1
}

cleanup
exit 0
