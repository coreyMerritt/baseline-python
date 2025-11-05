#!/usr/bin/env python3
from scripts.config_utils import ensure_logging_config_exists
from scripts.ensure_venv import ensure_venv
from scripts.install_dependencies import (
  install_core_dependencies,
  install_dev_dependencies,
  install_infra_dependencies,
  needs_dev_dependencies,
  needs_infra_dependencies
)

ensure_venv()
install_core_dependencies()
if needs_dev_dependencies():
  install_dev_dependencies()
if needs_infra_dependencies():
  install_infra_dependencies()
ensure_logging_config_exists()
# isort: off
from src.main import create_app  # pylint: disable=wrong-import-position
# isort: on
create_app()
