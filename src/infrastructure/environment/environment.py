import os

from dotenv import load_dotenv

from infrastructure.abc_infrastructure import Infrastructure


class Environment(Infrastructure):
  _first_call: bool = True

  @staticmethod
  def get_env_var(var_name: str) -> str | None:
    return os.getenv(var_name)

  @staticmethod
  def set_env_var(var_name: str, var_value: str) -> None:
    os.environ[var_name] = var_value

  @staticmethod
  def load_env() -> None:
    load_dotenv()
