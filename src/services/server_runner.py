import uvicorn

from infrastructure.config.config_manager import ConfigManager
from infrastructure.config.enums.environment import Environment
from infrastructure.config.exceptions.environment_exception import EnvironmentException
from infrastructure.config.mapping.environment_mapper import EnvironmentMapper


class ServerRunner:
  def run(self, env_str: str, host: str, port: int):
    env_enum = EnvironmentMapper.str_to_enum(env_str)
    ConfigManager.refresh_environment(env_str)
    if env_enum == Environment.DEV:
      uvicorn.run(
        "interfaces.rest.routers:create_app",
        host=host,
        port=port,
        reload=True,
        reload_excludes=[".venv/*", "*/__pycache__/*", "*.pyc", ".git"]
      )
    elif env_enum == Environment.PROD:
      uvicorn.run(
        "interfaces.rest.routers:create_app",
        host=host,
        port=port,
        reload=False
      )
    elif env_enum == Environment.TEST:
      uvicorn.run(
        "interfaces.rest.routers:create_app",
        host=host,
        port=port,
        reload=False
      )
    else:
      raise EnvironmentException()
