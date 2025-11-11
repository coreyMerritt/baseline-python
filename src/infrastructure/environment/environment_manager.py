import os

from dotenv import load_dotenv
from infrastructure.abc_infrastructure import Infrastructure
from infrastructure.environment.exceptions.unknown_environment_variable_exception import (
  UnknownEnvironmentVariableException
)


class EnvironmentManager(Infrastructure):
  _first_call: bool = True

  @staticmethod
  def get_env_var(var_name: str) -> str:
    if EnvironmentManager._first_call:
      EnvironmentManager._load_env()
      EnvironmentManager._first_call = False
    var_value = os.getenv(var_name)
    if not var_value:
      raise UnknownEnvironmentVariableException()
    return var_value

  @staticmethod
  def set_env_var(var_name: str, var_value: str) -> None:
    if EnvironmentManager._first_call:
      EnvironmentManager._load_env()
      EnvironmentManager._first_call = False
    os.environ[var_name] = var_value

  @staticmethod
  def _load_env() -> None:
    load_dotenv()
