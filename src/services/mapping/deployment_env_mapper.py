from services.enums.deployment_environment import DeploymentEnvironment
from services.exceptions.service_mapper_err import ServiceMapperErr


class DeploymentEnvMapper:
  @staticmethod
  def str_to_enum(string: str) -> DeploymentEnvironment:
    for enum in DeploymentEnvironment:
      if string.lower() == enum.value.lower():
        return enum
    raise ServiceMapperErr(string)
