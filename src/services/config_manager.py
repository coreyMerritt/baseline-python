from datetime import datetime, timedelta, timezone

from infrastructure.config.parser import ConfigParser
from infrastructure.disk.disk import Disk
from infrastructure.environment.environment import Environment
from services.abc_service import Service
from services.enums.environment_type import EnvironmentType
from services.exceptions.config_load_exception import ConfigLoadException
from services.exceptions.unset_environment_variable_exception import UnsetEnvironmentVariableException
from services.mapping.app_environment_mapper import AppEnvironmentMapper
from shared.models.configs.database_config import DatabaseConfig
from shared.models.configs.external_services.external_services_config import ExternalServicesConfig
from shared.models.configs.health_check_config import HealthCheckConfig
from shared.models.configs.logger_config import LoggerConfig
from shared.models.health_reports.config_health_report import ConfigHealthReport


# NOTE: Because LogManager needs configs from ConfigManager, ConfigManager shouldn't handle any logging
class ConfigManager(Service):
  _is_configured: bool = False
  _last_env_load: datetime | None = None
  _config_dir: str
  _database_config: DatabaseConfig
  _external_services_config: ExternalServicesConfig
  _health_check_config: HealthCheckConfig
  _logger_config: LoggerConfig

  @staticmethod
  def get_health_report() -> ConfigHealthReport:
    is_config_dir = ConfigManager._config_dir is not None
    is_configured = ConfigManager._is_configured
    is_database_config = ConfigManager._database_config is not None
    is_external_services_config = ConfigManager._external_services_config is not None
    is_health_check_config = ConfigManager._health_check_config is not None
    is_logger_config = ConfigManager._logger_config is not None
    healthy = (
      is_config_dir
      and is_configured
      and is_database_config
      and is_external_services_config
      and is_health_check_config
      and is_logger_config
    )
    return ConfigHealthReport(
      is_config_dir=is_config_dir,
      is_configured=is_configured,
      is_database_config=is_database_config,
      is_external_services_config=is_external_services_config,
      is_health_check_config=is_health_check_config,
      is_logger_config=is_logger_config,
      healthy=healthy
    )

  @staticmethod
  def refresh() -> None:
    env_enum = ConfigManager.get_env()
    Environment.load_env()
    ConfigManager._config_dir = f"./config/{env_enum.value}"
    ConfigManager.refresh_database_config()
    ConfigManager.refresh_external_services_config()
    ConfigManager.refresh_health_check_config()
    ConfigManager.refresh_logger_config()
    ConfigManager._is_configured = True

  @staticmethod
  def refresh_database_config() -> None:
    database_config_path = f"{ConfigManager._config_dir}/database.yml"
    try:
      raw_database_config = Disk().read_yaml(database_config_path)
    except Exception as e:
      raise ConfigLoadException(str(e)) from e
    ConfigManager._database_config = ConfigParser().parse_database_config(raw_database_config)

  @staticmethod
  def refresh_external_services_config() -> None:
    external_services_config_path = f"{ConfigManager._config_dir}/external_services.yml"
    try:
      raw_external_services_config = Disk().read_yaml(external_services_config_path)
    except Exception as e:
      raise ConfigLoadException(str(e)) from e
    ConfigManager._external_services_config = ConfigParser().parse_external_services_config(
      raw_external_services_config
    )

  @staticmethod
  def refresh_health_check_config() -> None:
    health_check_config_path = f"{ConfigManager._config_dir}/health_check.yml"
    try:
      raw_health_check_config = Disk().read_yaml(health_check_config_path)
    except Exception as e:
      raise ConfigLoadException(str(e)) from e
    ConfigManager._health_check_config = ConfigParser().parse_health_check_config(raw_health_check_config)

  @staticmethod
  def refresh_logger_config() -> None:
    logger_config_path = f"{ConfigManager._config_dir}/logger.yml"
    try:
      raw_logger_config = Disk().read_yaml(logger_config_path)
    except Exception as e:
      raise ConfigLoadException(str(e)) from e
    ConfigManager._logger_config = ConfigParser().parse_logger_config(raw_logger_config)

  @staticmethod
  def get_config_dir() -> str:
    return ConfigManager._config_dir

  @staticmethod
  def get_database_config() -> DatabaseConfig:
    if not ConfigManager._is_configured:
      ConfigManager.refresh()
    return ConfigManager._database_config

  @staticmethod
  def get_external_config() -> ExternalServicesConfig:
    if not ConfigManager._is_configured:
      ConfigManager.refresh()
    return ConfigManager._external_services_config

  @staticmethod
  def get_health_check_config() -> HealthCheckConfig:
    if not ConfigManager._is_configured:
      ConfigManager.refresh()
    return ConfigManager._health_check_config

  @staticmethod
  def get_logger_config() -> LoggerConfig:
    if not ConfigManager._is_configured:
      ConfigManager.refresh()
    return ConfigManager._logger_config

  @staticmethod
  def get_env() -> EnvironmentType:
    if ConfigManager._is_stale_env():
      Environment.load_env()
      ConfigManager._last_env_load = datetime.now(timezone.utc)
    env_str = Environment.get_env_var("PROJECTNAME_ENVIRONMENT")
    if not env_str:
      raise UnsetEnvironmentVariableException()
    env_enum = AppEnvironmentMapper.str_to_enum(env_str)
    return env_enum

  @staticmethod
  def set_env(env_str: str) -> None:
    Environment.set_env_var("PROJECTNAME_ENVIRONMENT", env_str)

  @staticmethod
  def _is_stale_env() -> bool:
    if not ConfigManager._last_env_load:
      return True
    return datetime.now(timezone.utc) - ConfigManager._last_env_load > timedelta(seconds=3600)
