from services.enums.deployment_environment import DeploymentEnvironment
from shared.exceptions.mapper_err import MapperErr


class DeploymentEnvMapper:
  @staticmethod
  def str_to_enum(string: str) -> DeploymentEnvironment:
    for enum in DeploymentEnvironment:
      if string.lower() == enum.value.lower():
        return enum
    raise MapperErr()
