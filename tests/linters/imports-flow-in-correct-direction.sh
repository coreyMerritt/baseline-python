#!/usr/bin/env bash

set -o pipefail
set -u
set -x

function importCheck() {
  layer="$1"    # ex) infrastructure
  import="$2"   # ex) domain
  exception="${3-}"   # ex) mapper
  if [[ -n "$exception" ]]; then
    echo -e "\n\n\n\t========== $layer may not import from $import, UNLESS they are ${exception}s ==========\n"
    grep --color -rn " ${import}\." "src/${layer}/" --exclude-dir="__pycache__" \
      | awk "!(/\/${exception}s\// && /${exception}\.py/)" \
      | grep --color=always -E "src/${layer}|${import}\." \
      && exit 1
  else
    echo -e "\n\n\n\t========== $layer may not import from $import ==========\n"
    grep --color -rn " ${import}\." "src/${layer}/" --exclude-dir="__pycache__" \
      | grep --color=always -E "src/${layer}|${import}\." \
      && exit 1
  fi
}

# Tests
importCheck "interfaces/rest/health/controllers" "infrastructure"
importCheck "interfaces/rest/health/dtos" "infrastructure"
importCheck "interfaces/rest/health/routes" "infrastructure"
importCheck "interfaces/rest/v1/controllers" "infrastructure"
importCheck "interfaces/rest/v1/dtos" "infrastructure"
importCheck "interfaces/rest/v1/routes" "infrastructure"
importCheck "interfaces/command_line" "infrastructure"
importCheck "services" "interfaces"
importCheck "infrastructure" "services"
importCheck "infrastructure" "interfaces"
importCheck "domain" "infrastructure"
importCheck "domain" "services"
importCheck "domain" "interfaces"

exit 0
