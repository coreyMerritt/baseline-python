import os

import uvicorn

from services.enums.deployment_environment import DeploymentEnvironment
from services.enums.env_var import EnvVar
from services.exceptions.service_mapper_err import ServiceMapperErr
from services.mapping.deployment_env_mapper import DeploymentEnvMapper


def run_webserver(env_str: str, host: str, port: int):
  env_enum = DeploymentEnvMapper.str_to_enum(env_str)
  os.environ[EnvVar.DEPLOYMENT_ENVIRONMENT.value] = env_str
  if env_enum == DeploymentEnvironment.DEV:
    uvicorn.run(
      "interfaces.rest.webserver_hook:create_app",
      factory=True,
      host=host,
      port=port,
      reload=True,
      reload_excludes=[".venv/*", "*/__pycache__/*", "*.pyc", ".git"]
    )
  elif env_enum == DeploymentEnvironment.PROD:
    uvicorn.run(
      "interfaces.rest.webserver_hook:create_app",
      factory=True,
      host=host,
      port=port,
      reload=False
    )
  elif env_enum == DeploymentEnvironment.TEST:
    uvicorn.run(
      "interfaces.rest.webserver_hook:create_app",
      factory=True,
      host=host,
      port=port,
      reload=False
    )
  else:
    raise ServiceMapperErr()
