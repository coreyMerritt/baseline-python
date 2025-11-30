import os
from typing import TypeVar, cast

from infrastructure.environment.models.env_var import EnvVar
from infrastructure.logger.projectname_logger import ProjectnameLogger
from shared.exceptions.undocumented_case_err import UndocumentedCaseErr

T = TypeVar("T")

def get_final_config_var(logger: ProjectnameLogger, config_var: T, env_var: EnvVar) -> T:
  override = os.getenv(env_var.value)
  if override:
    if isinstance(config_var, str):
      return cast(T, str(override))
    if isinstance(config_var, int):
      return cast(T, int(override))
    if isinstance(config_var, float):
      return cast(T, float(override))
    raise UndocumentedCaseErr()
  logger.warning(f"No override found, using config file for: {env_var.value}", error=None)
  return config_var
