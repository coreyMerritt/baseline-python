import uvicorn

from services.config_manager import ConfigManager
from services.enums.deployment_environment import DeploymentEnvironment
from services.exceptions.environment_exception import EnvironmentException
from services.mapping.deployment_env_mapper import DeploymentEnvMapper


def run_server(env_str: str, host: str, port: int):
  env_enum = DeploymentEnvMapper.str_to_enum(env_str)
  ConfigManager.set_env(env_enum)
  ConfigManager.refresh()
  env_str = ConfigManager.get_env()
  if env_enum == DeploymentEnvironment.DEV:
    uvicorn.run(
      "interfaces.rest.webserver_entrypoint:create_app",
      host=host,
      port=port,
      reload=True,
      reload_excludes=[".venv/*", "*/__pycache__/*", "*.pyc", ".git"]
    )
  elif env_enum == DeploymentEnvironment.PROD:
    uvicorn.run(
      "interfaces.rest.webserver_entrypoint:create_app",
      host=host,
      port=port,
      reload=False
    )
  elif env_enum == DeploymentEnvironment.TEST:
    uvicorn.run(
      "interfaces.rest.webserver_entrypoint:create_app",
      host=host,
      port=port,
      reload=False
    )
  else:
    raise EnvironmentException()
