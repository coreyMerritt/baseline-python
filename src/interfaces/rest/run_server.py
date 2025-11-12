import uvicorn

from services.config_manager import ConfigManager
from services.enums.environment_type import EnvironmentType
from services.exceptions.environment_exception import EnvironmentException
from services.mapping.app_environment_mapper import AppEnvironmentMapper


def run_server(env_str: str, host: str, port: int):
  ConfigManager.set_env(env_str)
  ConfigManager.refresh()
  env_str = ConfigManager.get_env()
  env_enum = AppEnvironmentMapper.str_to_enum(env_str)
  if env_enum == EnvironmentType.DEV:
    uvicorn.run(
      "interfaces.rest.webserver_entrypoint:create_app",
      host=host,
      port=port,
      reload=True,
      reload_excludes=[".venv/*", "*/__pycache__/*", "*.pyc", ".git"]
    )
  elif env_enum == EnvironmentType.PROD:
    uvicorn.run(
      "interfaces.rest.webserver_entrypoint:create_app",
      host=host,
      port=port,
      reload=False
    )
  elif env_enum == EnvironmentType.TEST:
    uvicorn.run(
      "interfaces.rest.webserver_entrypoint:create_app",
      host=host,
      port=port,
      reload=False
    )
  else:
    raise EnvironmentException()
