from infrastructure.config.enums.environment import Environment
from infrastructure.config.exceptions.environment_exception import EnvironmentException


class AppEnvironmentMapper:
  @staticmethod
  def str_to_enum(string: str) -> Environment:
    for enum in Environment:
      if string.lower() == enum.value.lower():
        return enum
    raise EnvironmentException(string)

  @staticmethod
  def enum_to_str(enum: Environment) -> str:
    return enum.value
