#!/usr/bin/env bash

set -e
set -E
set -o pipefail
set -u
set -x

grep \
  --color \
  --recursive \
  --line-number \
  --ignore-case \
  --exclude-dir "*cache*" \
  --exclude-dir "*egg-info*" \
  --exclude-dir ".git" \
  --exclude-dir ".venv" \
  "projectname" \
  . 2>/dev/null
