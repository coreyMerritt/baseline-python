from services.enums.deployment_env import DeploymentEnv
from services.exceptions.environment_exception import EnvironmentException


class DeploymentEnvMapper:
  @staticmethod
  def str_to_enum(string: str) -> DeploymentEnv:
    for enum in DeploymentEnv:
      if string.lower() == enum.value.lower():
        return enum
    raise EnvironmentException(string)
