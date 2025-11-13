from services.enums.deployment_environment import DeploymentEnvironment
from services.exceptions.deployment_environment_exception import DeploymentEnvironmentException


class DeploymentEnvMapper:
  @staticmethod
  def str_to_enum(string: str) -> DeploymentEnvironment:
    for enum in DeploymentEnvironment:
      if string.lower() == enum.value.lower():
        return enum
    raise DeploymentEnvironmentException(string)
