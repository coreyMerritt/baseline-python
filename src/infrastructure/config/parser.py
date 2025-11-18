from typing import Any

from dacite import Config, from_dict

from infrastructure.base_infrastructure import Infrastructure
from infrastructure.config.exceptions.config_parser_err import ConfigParserErr
from shared.enums.logger_level import LoggerLevel
from shared.enums.timezone import Timezone
from shared.models.configs.database_config import DatabaseConfig
from shared.models.configs.disk_config import DiskConfig
from shared.models.configs.external_services_config import ExternalServicesConfig
from shared.models.configs.health_check_config import HealthCheckConfig
from shared.models.configs.logger_config import LoggerConfig
from shared.models.health_reports.config_parser_health_report import ConfigParserHealthReport


class ConfigParser(Infrastructure):
  def get_health_report(self) -> ConfigParserHealthReport:
    return ConfigParserHealthReport(
      healthy=True
    )

  def parse_database_config(self, some_data: Any) -> DatabaseConfig:
    try:
      return from_dict(
        data_class=DatabaseConfig,
        data=some_data,
        config=Config(
          strict=True
        )
      )
    except Exception as e:
      raise ConfigParserErr(
        config_name="Database Config"
      ) from e

  def parse_disk_config(self, some_data: Any) -> DiskConfig:
    try:
      return from_dict(
        data_class=DiskConfig,
        data=some_data,
        config=Config(
          strict=True
        )
      )
    except Exception as e:
      raise ConfigParserErr(
        config_name="Disk Config"
      ) from e

  def parse_external_services_config(self, some_data: Any) -> ExternalServicesConfig:
    try:
      return from_dict(
        data_class=ExternalServicesConfig,
        data=some_data,
        config=Config(
          strict=True
        )
      )
    except Exception as e:
      raise ConfigParserErr(
        config_name="External Services Config"
      ) from e

  def parse_health_check_config(self, some_data: Any) -> HealthCheckConfig:
    try:
      return from_dict(
        data_class=HealthCheckConfig,
        data=some_data,
        config=Config(
          strict=True
        )
      )
    except Exception as e:
      raise ConfigParserErr(
        config_name="Health Check Config"
      ) from e

  def parse_logger_config(self, some_data: Any) -> LoggerConfig:
    try:
      return from_dict(
        data_class=LoggerConfig,
        data=some_data,
        config=Config(
          strict=True,
          type_hooks={
            LoggerLevel: LoggerLevel,
            Timezone: Timezone,
          }
        ),
      )
    except Exception as e:
      raise ConfigParserErr(
        config_name="Logger Config"
      ) from e
