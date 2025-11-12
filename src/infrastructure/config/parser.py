from typing import Any

from dacite import Config, from_dict

from infrastructure.abc_infrastructure import Infrastructure
from infrastructure.config.exceptions.config_parser_exception import ConfigParserException
from shared.enums.logging_level import LoggingLevel
from shared.models.configs.database_config import DatabaseConfig
from shared.models.configs.external_services.external_services_config import ExternalServicesConfig
from shared.models.configs.health_check_config import HealthCheckConfig
from shared.models.configs.logging_config import LoggingConfig


class ConfigParser(Infrastructure):
  def parse_database_config(self, some_data: Any) -> DatabaseConfig:
    try:
      return from_dict(
        data_class=DatabaseConfig,
        data=some_data
      )
    except Exception as e:
      raise ConfigParserException(str(e)) from e

  def parse_external_services_config(self, some_data: Any) -> ExternalServicesConfig:
    try:
      return from_dict(
        data_class=ExternalServicesConfig,
        data=some_data
      )
    except Exception as e:
      raise ConfigParserException(str(e)) from e

  def parse_health_check_config(self, some_data: Any) -> HealthCheckConfig:
    try:
      return from_dict(
        data_class=HealthCheckConfig,
        data=some_data
      )
    except Exception as e:
      raise ConfigParserException(str(e)) from e

  def parse_logging_config(self, some_data: Any) -> LoggingConfig:
    try:
      return from_dict(
        data_class=LoggingConfig,
        data=some_data,
        config=Config(type_hooks={LoggingLevel: LoggingLevel})
      )
    except Exception as e:
      raise ConfigParserException(str(e)) from e
