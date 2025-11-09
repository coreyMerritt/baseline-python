import uvicorn

from infrastructure.config.config_manager import ConfigManager
from infrastructure.config.enums.environment import Environment
from infrastructure.config.exceptions.environment_exception import EnvironmentException
from infrastructure.config.mapping.environment_mapper import EnvironmentMapper


class ServerRunner:
  def run(self, env: str, host: str, port: int):
    env_enum = EnvironmentMapper.str_to_enum(env)
    ConfigManager.refresh_configs()
    ConfigManager.set_environment(env_enum)
    if env == Environment.DEV:
      uvicorn.run(
        "interfaces.rest.routers:create_app",
        host=host,
        port=port,
        reload=True,
        reload_excludes=[".venv/*", "*/__pycache__/*", "*.pyc", ".git"]
      )
    elif env == Environment.PROD:
      uvicorn.run(
        "interfaces.rest.routers:create_app",
        host=host,
        port=port,
        reload=False
      )
    elif env == Environment.TEST:
      uvicorn.run(
        "interfaces.rest.routers:create_app",
        host=host,
        port=port,
        reload=False
      )
    else:
      raise EnvironmentException()
