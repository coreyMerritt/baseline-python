import uvicorn

from infrastructure.config.enums.environment import Environment
from infrastructure.config.exceptions.environment_exception import EnvironmentException
from infrastructure.config.mapping.app_environment_mapper import AppEnvironmentMapper
from infrastructure.environment.environment_manager import EnvironmentManager
from services.abc_service import Service


class ServerRunner(Service):
  def run(self, host: str, port: int):
    env_str = EnvironmentManager.get_env_var("PROJECTNAME_ENVIRONMENT")
    env_enum = AppEnvironmentMapper.str_to_enum(env_str)
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
