from services.enums.deployment_environment import DeploymentEnvironment
from services.exceptions.environment_exception import EnvironmentException


class DeploymentEnvMapper:
  @staticmethod
  def str_to_enum(string: str) -> DeploymentEnvironment:
    for enum in DeploymentEnvironment:
      if string.lower() == enum.value.lower():
        return enum
    raise EnvironmentException(string)
