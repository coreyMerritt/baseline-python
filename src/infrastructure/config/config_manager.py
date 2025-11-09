import os
import sys

import yaml
from dacite import Config, from_dict
from dotenv import load_dotenv

from infrastructure.config.enums.environment import Environment
from infrastructure.config.enums.logging_level import LoggingLevel
from infrastructure.config.exceptions.config_load_exception import ConfigLoadException
from infrastructure.config.exceptions.config_parse_exception import ConfigParseException
from infrastructure.config.exceptions.using_config_before_loaded_exception import UsingConfigBeforeLoadedException
from infrastructure.config.mapping.environment_mapper import EnvironmentMapper
from infrastructure.config.models.database_config import DatabaseConfig
from infrastructure.config.models.health_check_config import HealthCheckConfig
from infrastructure.config.models.logging_config import LoggingConfig


# NOTE: Because LogManager reaches to ConfigManager, ConfigManager shouldn't handle any logging
class ConfigManager:
  _is_configured: bool = False
  _environment: Environment
  _config_dir: str
  _database_config: DatabaseConfig
  _health_check_config: HealthCheckConfig
  _logging_config: LoggingConfig

  @staticmethod
  def refresh_environment(env_str: str) -> None:
    load_dotenv()
    env_enum = EnvironmentMapper.str_to_enum(env_str)
    ConfigManager._environment = env_enum
    ConfigManager._config_dir = f"./config/{ConfigManager._environment.value}"
    ConfigManager.refresh_database_config()
    ConfigManager.refresh_health_check_config()
    ConfigManager.refresh_logging_config()
    ConfigManager._is_configured = True

  @staticmethod
  def refresh_database_config() -> None:
    database_config_path = f"{ConfigManager._config_dir}/database.yml"
    try:
      with open(database_config_path, "r", encoding='utf-8') as database_config_file:
        raw_database_config = yaml.safe_load(database_config_file)
    except Exception as e:
      raise ConfigLoadException() from e
    try:
      ConfigManager._database_config = from_dict(
        data_class=DatabaseConfig,
        data=raw_database_config
      )
    except Exception as e:
      raise ConfigParseException() from e

  @staticmethod
  def refresh_health_check_config() -> None:
    health_check_config_path = f"{ConfigManager._config_dir}/health_check.yml"
    try:
      with open(health_check_config_path, "r", encoding='utf-8') as health_check_config_file:
        raw_health_check_config = yaml.safe_load(health_check_config_file)
    except Exception as e:
      raise ConfigLoadException() from e
    try:
      ConfigManager._health_check_config = from_dict(
        data_class=HealthCheckConfig,
        data=raw_health_check_config
      )
    except Exception as e:
      raise ConfigParseException() from e

  @staticmethod
  def refresh_logging_config() -> None:
    logging_config_path = f"{ConfigManager._config_dir}/logging.yml"
    dacite_config = Config(type_hooks={LoggingLevel: LoggingLevel})
    try:
      with open(logging_config_path, "r", encoding='utf-8') as logging_config_file:
        raw_logging_config = yaml.safe_load(logging_config_file)
    except Exception as e:
      raise ConfigLoadException() from e
    try:
      ConfigManager._logging_config = from_dict(
        data_class=LoggingConfig,
        data=raw_logging_config,
        config=dacite_config
      )
    except Exception as e:
      raise ConfigParseException() from e

  @staticmethod
  def is_configured() -> bool:
    return ConfigManager._is_configured

  @staticmethod
  def is_environment() -> bool:
    return ConfigManager._environment is not None

  @staticmethod
  def is_config_dir() -> bool:
    return ConfigManager._config_dir is not None

  @staticmethod
  def is_database_config() -> bool:
    return ConfigManager._database_config is not None

  @staticmethod
  def is_health_check_config() -> bool:
    return ConfigManager._health_check_config is not None

  @staticmethod
  def is_logging_config() -> bool:
    return ConfigManager._logging_config is not None

  @staticmethod
  def get_environment() -> Environment:
    return ConfigManager._environment

  @staticmethod
  def get_config_dir() -> str:
    return ConfigManager._config_dir

  @staticmethod
  def get_database_config() -> DatabaseConfig:
    if not ConfigManager._is_configured:
      raise UsingConfigBeforeLoadedException()
    return ConfigManager._database_config

  @staticmethod
  def get_health_check_config() -> HealthCheckConfig:
    if not ConfigManager._is_configured:
      raise UsingConfigBeforeLoadedException()
    return ConfigManager._health_check_config

  @staticmethod
  def get_logging_config() -> LoggingConfig:
    if not ConfigManager._is_configured:
      raise UsingConfigBeforeLoadedException()
    return ConfigManager._logging_config

  @staticmethod
  def set_environment(environment: str) -> None:
    env_enum = EnvironmentMapper.str_to_enum(environment)
    ConfigManager._environment = env_enum
    ConfigManager._config_dir = f"./config/{ConfigManager._environment.value}"
    ConfigManager.refresh_database_config()
    ConfigManager.refresh_health_check_config()
    ConfigManager.refresh_logging_config()
    ConfigManager._is_configured = True

  @staticmethod
  def _get_env_var_safe(var_name: str) -> str:
    var_value = os.getenv(var_name)
    if not var_value:
      print(f"\n\tSet {var_name} and try again.")
      sys.exit(1)
    return var_value
