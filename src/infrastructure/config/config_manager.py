import yaml
from dacite import Config, from_dict

from infrastructure.abc_infrastructure import Infrastructure
from infrastructure.config.enums.environment import Environment
from infrastructure.config.enums.logging_level import LoggingLevel
from infrastructure.config.exceptions.config_load_exception import ConfigLoadException
from infrastructure.config.exceptions.config_parse_exception import ConfigParseException
from infrastructure.config.mapping.app_environment_mapper import AppEnvironmentMapper
from infrastructure.config.models.config_health_report import ConfigHealthReport
from infrastructure.config.models.database_config import DatabaseConfig
from infrastructure.config.models.external_config import ExternalConfig
from infrastructure.config.models.health_check_config import HealthCheckConfig
from infrastructure.config.models.logging_config import LoggingConfig
from infrastructure.environment.environment_manager import EnvironmentManager


# NOTE: Because LogManager reaches to ConfigManager, ConfigManager shouldn't handle any logging
class ConfigManager(Infrastructure):
  _is_configured: bool = False
  _environment: Environment
  _config_dir: str
  _database_config: DatabaseConfig
  _external_config: ExternalConfig
  _health_check_config: HealthCheckConfig
  _logging_config: LoggingConfig

  @staticmethod
  def get_health_report() -> ConfigHealthReport:
    is_config_dir = ConfigManager._config_dir is not None
    is_configured = ConfigManager._is_configured
    is_database_config = ConfigManager._database_config is not None
    is_environment = ConfigManager._environment is not None
    is_health_check_config = ConfigManager._health_check_config is not None
    is_logging_config = ConfigManager._logging_config is not None
    healthy = (
      is_config_dir
      and is_configured
      and is_database_config
      and is_environment
      and is_health_check_config
      and is_logging_config
    )
    return ConfigHealthReport(
      is_config_dir=is_config_dir,
      is_configured=is_configured,
      is_database_config=is_database_config,
      is_environment=is_environment,
      is_health_check_config=is_health_check_config,
      is_logging_config=is_logging_config,
      healthy=healthy
    )

  @staticmethod
  def refresh() -> None:
    env_str = EnvironmentManager.get_env_var("PROJECTNAME_ENVIRONMENT")
    env_enum = AppEnvironmentMapper.str_to_enum(env_str)
    ConfigManager._environment = env_enum
    ConfigManager._config_dir = f"./config/{ConfigManager._environment.value}"
    ConfigManager.refresh_database_config()
    ConfigManager.refresh_external_config()
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
      raise ConfigLoadException(str(e)) from e
    try:
      ConfigManager._database_config = from_dict(
        data_class=DatabaseConfig,
        data=raw_database_config
      )
    except Exception as e:
      raise ConfigParseException(str(e)) from e

  @staticmethod
  def refresh_external_config() -> None:
    external_config_path = f"{ConfigManager._config_dir}/external.yml"
    try:
      with open(external_config_path, "r", encoding='utf-8') as external_config_file:
        raw_external_config = yaml.safe_load(external_config_file)
    except Exception as e:
      raise ConfigLoadException(str(e)) from e
    try:
      ConfigManager._external_config = from_dict(
        data_class=ExternalConfig,
        data=raw_external_config
      )
    except Exception as e:
      raise ConfigParseException(str(e)) from e

  @staticmethod
  def refresh_health_check_config() -> None:
    health_check_config_path = f"{ConfigManager._config_dir}/health_check.yml"
    try:
      with open(health_check_config_path, "r", encoding='utf-8') as health_check_config_file:
        raw_health_check_config = yaml.safe_load(health_check_config_file)
    except Exception as e:
      raise ConfigLoadException(str(e)) from e
    try:
      ConfigManager._health_check_config = from_dict(
        data_class=HealthCheckConfig,
        data=raw_health_check_config
      )
    except Exception as e:
      raise ConfigParseException(str(e)) from e

  @staticmethod
  def refresh_logging_config() -> None:
    logging_config_path = f"{ConfigManager._config_dir}/logging.yml"
    dacite_config = Config(type_hooks={LoggingLevel: LoggingLevel})
    try:
      with open(logging_config_path, "r", encoding='utf-8') as logging_config_file:
        raw_logging_config = yaml.safe_load(logging_config_file)
    except Exception as e:
      raise ConfigLoadException(str(e)) from e
    try:
      ConfigManager._logging_config = from_dict(
        data_class=LoggingConfig,
        data=raw_logging_config,
        config=dacite_config
      )
    except Exception as e:
      raise ConfigParseException(str(e)) from e

  @staticmethod
  def get_environment() -> Environment:
    return ConfigManager._environment

  @staticmethod
  def get_config_dir() -> str:
    return ConfigManager._config_dir

  @staticmethod
  def get_database_config() -> DatabaseConfig:
    if not ConfigManager._is_configured:
      ConfigManager.refresh()
    return ConfigManager._database_config

  @staticmethod
  def get_external_config() -> ExternalConfig:
    if not ConfigManager._is_configured:
      ConfigManager.refresh()
    return ConfigManager._external_config

  @staticmethod
  def get_health_check_config() -> HealthCheckConfig:
    if not ConfigManager._is_configured:
      ConfigManager.refresh()
    return ConfigManager._health_check_config

  @staticmethod
  def get_logging_config() -> LoggingConfig:
    if not ConfigManager._is_configured:
      ConfigManager.refresh()
    return ConfigManager._logging_config
