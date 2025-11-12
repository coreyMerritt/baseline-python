#!/usr/bin/env bash

set -e
set -o pipefail
set -x

echo "Interfaces may not import from infrastructure"
grep --color -rn "infrastructure\." src/interfaces/ --exclude-dir="__pycache__" && exit 1

echo "Interfaces may not import from domain, UNLESS they are adapters"
grep --color -rn "domain\." src/interfaces/ --exclude-dir="__pycache__" | awk '!(/\/adapters\// && /adapter\.py/)' | grep . && exit 1

echo "Services may not import from interfaces"
grep --color -rn "interfaces\." src/services/ --exclude-dir="__pycache__" && exit 1

echo "Domain may not import from infrastructure"
grep --color -rn "infrastructure\." src/domain/ --exclude-dir="__pycache__" && exit 1

echo "Domain may not import from services"
grep --color -rn "services\." src/domain/ --exclude-dir="__pycache__" && exit 1

echo "Domain may not import from interfaces"
grep --color -rn "interfaces\." src/domain/ --exclude-dir="__pycache__" && exit 1

echo "Infrastructure may not import from Domain"
grep --color -rn "domain\." src/infrastructure/ --exclude-dir="__pycache__" && exit 1

echo "Infrastructure may not import from Services"
grep --color -rn "services\." src/infrastructure/ --exclude-dir="__pycache__" && exit 1

echo "Infrastructure may not import from Interfaces"
grep --color -rn "interfaces\." src/infrastructure/ --exclude-dir="__pycache__" && exit 1
