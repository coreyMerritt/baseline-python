import yaml
from dacite import Config, from_dict

from infrastructure.config.enums.logging_level import LoggingLevel
from infrastructure.config.exceptions.config_load_exception import ConfigLoadException
from infrastructure.config.exceptions.config_parse_exception import ConfigParseException
from infrastructure.config.models.database_config import DatabaseConfig
from infrastructure.config.models.logging_config import LoggingConfig


# NOTE: Because LogManager reaches to ConfigManager, ConfigManager shouldn't handle any logging
class ConfigManager:
  _is_configured: bool = False
  _database_config: DatabaseConfig
  _logging_config: LoggingConfig

  @staticmethod
  def refresh_configs() -> None:
    ConfigManager.refresh_database_config()
    ConfigManager.refresh_logging_config()

  @staticmethod
  def refresh_database_config() -> None:
    try:
      with open("config/prod/database.yml", "r", encoding='utf-8') as database_config_file:
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
  def refresh_logging_config() -> None:
    dacite_config = Config(type_hooks={LoggingLevel: LoggingLevel})
    try:
      with open("config/prod/logging.yml", "r", encoding='utf-8') as logging_config_file:
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
  def get_database_config() -> DatabaseConfig:
    if not ConfigManager._is_configured:
      ConfigManager.refresh_configs()
      ConfigManager._is_configured = True
    return ConfigManager._database_config

  @staticmethod
  def get_logging_config() -> LoggingConfig:
    if not ConfigManager._is_configured:
      ConfigManager.refresh_configs()
      ConfigManager._is_configured = True
    return ConfigManager._logging_config

ConfigManager.refresh_configs()
