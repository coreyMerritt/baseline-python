#!/usr/bin/env python3
import os
from dotenv import load_dotenv
import uvicorn
import yaml

from utilities.get_project_name import get_project_name
from utilities.get_project_root import get_project_root


def main():
  # Vars
  load_dotenv()
  PROJECT_NAME = get_project_name()
  PROJECT_ROOT = get_project_root()
  ENVIRONMENT = os.getenv(f"{PROJECT_NAME}_ENVIRONMENT")
  assert ENVIRONMENT

  # Uvicorn
  UVICORN_CONFIG_PATH = f"{PROJECT_ROOT}/config/{ENVIRONMENT}/uvicorn.yml"
  with open(UVICORN_CONFIG_PATH, "r", encoding='utf-8') as uvicorn_config_file:
    UVICORN_CONFIG = yaml.safe_load(uvicorn_config_file)
  uvicorn.run(
    "src.main:app",
    host=UVICORN_CONFIG["host"],
    port=UVICORN_CONFIG["port"],
    reload=True,
    reload_excludes=[".venv/*", "*/__pycache__/*", "*.pyc", ".git"]
  )

if __name__ == "__main__":
  main()
