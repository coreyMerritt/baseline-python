import os

import uvicorn

from composition.enums.deployment_environment import DeploymentEnvironment
from composition.mappers.deployment_environment_mapper import DeploymentEnvironmentMapper
from infrastructure.environment.models.env_var import EnvVar
from shared.exceptions.undocumented_case_err import UndocumentedCaseErr


def run_webserver(env_str: str, host: str, port: int):
  # Inject deployment environment
  os.environ[EnvVar.DEPLOYMENT_ENVIRONMENT.value] = env_str
  # Determine whether to reload or not
  WEBSERVER_ENTRYPOINT = "composition.webserver.hook:create_app"
  env_enum = DeploymentEnvironmentMapper.str_to_enum(env_str)
  if env_enum == DeploymentEnvironment.DEV:
    RELOAD = True
    RELOAD_EXCLUDES = [".venv/*", "*/__pycache__/*", "*.pyc", ".git"]
  elif env_enum == DeploymentEnvironment.PROD:
    RELOAD = False
    RELOAD_EXCLUDES = []
  elif env_enum == DeploymentEnvironment.TEST:
    RELOAD = False
    RELOAD_EXCLUDES = []
  else:
    raise UndocumentedCaseErr()
  # Call webserver
  uvicorn.run(
    WEBSERVER_ENTRYPOINT,
    factory=True,
    host=host,
    port=port,
    reload=RELOAD,
    reload_excludes=RELOAD_EXCLUDES
  )
