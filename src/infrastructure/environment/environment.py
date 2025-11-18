import os

from dotenv import load_dotenv

from infrastructure.abc_infrastructure import Infrastructure
from infrastructure.environment.exceptions.unset_environment_variable_err import UnsetEnvironmentVariableErr


class Environment(Infrastructure):
  _first_call: bool = True

  @staticmethod
  def get_env_var(env_var_name: str) -> str:
    try:
      env_var = os.getenv(env_var_name)
      if env_var is None:
        raise TypeError("env_var is None")
      return env_var
    except Exception as e:
      raise UnsetEnvironmentVariableErr(
        env_var_name=env_var_name
      ) from e

  @staticmethod
  def set_env_var(env_var_name: str, var_value: str) -> None:
    os.environ[env_var_name] = var_value

  @staticmethod
  def load_env() -> None:
    load_dotenv()
