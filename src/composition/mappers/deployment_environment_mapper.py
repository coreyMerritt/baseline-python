from composition.enums.deployment_environment import DeploymentEnvironment
from shared.exceptions.enum_conversion_err import EnumConversionErr


class DeploymentEnvironmentMapper:
  @staticmethod
  def str_to_enum(string: str) -> DeploymentEnvironment:
    for enum in DeploymentEnvironment:
      if string.lower() == enum.value.lower():
        return enum
    raise EnumConversionErr(string)
