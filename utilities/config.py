import os
import shutil
from dotenv import load_dotenv

from utilities.get_project_root import get_project_root


def ensure_all_simple_configs_exist():
  ensure_logging_config_exists()
  ensure_uvicorn_config_exists()

def ensure_logging_config_exists():
  PROJECT_ROOT = get_project_root()
  load_dotenv()
  ENVIRONMENT = os.getenv("PROJECTNAME_ENVIRONMENT")
  model_logging_config_path = f"{PROJECT_ROOT}/config/model/logging.yml"
  logging_config_path = f"{PROJECT_ROOT}/config/{ENVIRONMENT}/logging.yml"
  if not os.path.isfile(logging_config_path):
    shutil.copy(model_logging_config_path, logging_config_path)

def ensure_uvicorn_config_exists():
  PROJECT_ROOT = get_project_root()
  load_dotenv()
  ENVIRONMENT = os.getenv("PROJECTNAME_ENVIRONMENT")
  model_logging_config_path = f"{PROJECT_ROOT}/config/model/uvicorn.yml"
  logging_config_path = f"{PROJECT_ROOT}/config/{ENVIRONMENT}/uvicorn.yml"
  if not os.path.isfile(logging_config_path):
    shutil.copy(model_logging_config_path, logging_config_path)
