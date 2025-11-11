from services.exceptions.environment_exception import EnvironmentException
from services.enums.environment import Environment


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
