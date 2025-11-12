from services.enums.environment_type import EnvironmentType
from services.exceptions.environment_exception import EnvironmentException


class AppEnvironmentMapper:
  @staticmethod
  def str_to_enum(string: str) -> EnvironmentType:
    for enum in EnvironmentType:
      if string.lower() == enum.value.lower():
        return enum
    raise EnvironmentException(string)

  @staticmethod
  def enum_to_str(enum: EnvironmentType) -> str:
    return enum.value
