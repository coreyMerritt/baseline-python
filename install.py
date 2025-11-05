#!/usr/bin/env python3
from scripts.install_dependencies import install_dependencies
from utilities.config import ensure_all_simple_configs_exist
from utilities.ensure_venv import ensure_venv


# General environment needs
ensure_venv()
install_dependencies()
ensure_all_simple_configs_exist()
