import uvicorn

from infrastructure.environment.environment_manager import EnvironmentManager
from services.config_manager import ConfigManager
from services.enums.environment import Environment
from services.exceptions.environment_exception import EnvironmentException
from services.mapping.app_environment_mapper import AppEnvironmentMapper


def run_server(env_str: str, host: str, port: int):
  EnvironmentManager.set_env_var("PROJECTNAME_ENVIRONMENT", env_str)
  ConfigManager.refresh()
  env_str = EnvironmentManager.get_env_var("PROJECTNAME_ENVIRONMENT")
  env_enum = AppEnvironmentMapper.str_to_enum(env_str)
  if env_enum == Environment.DEV:
    uvicorn.run(
      "interfaces.rest.webserver_entrypoint:create_app",
      host=host,
      port=port,
      reload=True,
      reload_excludes=[".venv/*", "*/__pycache__/*", "*.pyc", ".git"]
    )
  elif env_enum == Environment.PROD:
    uvicorn.run(
      "interfaces.rest.webserver_entrypoint:create_app",
      host=host,
      port=port,
      reload=False
    )
  elif env_enum == Environment.TEST:
    uvicorn.run(
      "interfaces.rest.webserver_entrypoint:create_app",
      host=host,
      port=port,
      reload=False
    )
  else:
    raise EnvironmentException()
