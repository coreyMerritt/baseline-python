#!/usr/bin/env bash

set -o pipefail
set -u
set -x

function importCheck() {
  layer="$1"    # ex) infrastructure
  import="$2"   # ex) domain
  exception="${3-}"   # ex) adapter|mapper
  if [[ -n "$exception" ]]; then
    echo -e "\n\t========== $layer may not import from $import, UNLESS they are ${exception}s =========="
    grep --color -rn "${import}\." src/${layer}/ --exclude-dir="__pycache__" \
      | awk "!(/\/${exception}s\// && /${exception}\.py/)" \
      | grep --color=always -E "src/${layer}|${import}\." \
      && exit 1
  else
    echo -e "\n\t========== $layer may not import from $import =========="
    grep --color -rn "${import}\." src/${layer}/ --exclude-dir="__pycache__" \
      | grep --color=always -E "src/${layer}|${import}\." \
      && exit 1
  fi
}

importCheck "interfaces" "infrastructure"
importCheck "interfaces" "infrastructure" "adapter"
importCheck "services" "interfaces"
importCheck "domain" "infrastructure"
importCheck "domain" "services"
importCheck "domain" "interfaces"
importCheck "infrastructure" "domain" "mapper"
importCheck "infrastructure" "services"
importCheck "infrastructure" "interfaces"
