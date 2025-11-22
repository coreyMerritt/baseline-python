from typing import Any

from dacite import Config, from_dict

from infrastructure.base_infrastructure import BaseInfrastructure
from infrastructure.config.exceptions.config_parser_err import ConfigParserErr
from infrastructure.cpu.models.cpu_config import CpuConfig
from infrastructure.database.models.database_config import DatabaseConfig
from infrastructure.disk.models.disk_config import DiskConfig
from infrastructure.external_services.models.external_services_config import ExternalServicesConfig
from infrastructure.external_services.models.typicode_config import TypicodeConfig
from infrastructure.logger.models.logger_config import LoggerConfig
from infrastructure.memory.models.memory_config import MemoryConfig
from shared.enums.logger_level import LoggerLevel
from shared.enums.timezone import Timezone
from shared.models.health_reports.config_parser_health_report import ConfigParserHealthReport


class ConfigParser(BaseInfrastructure):
  def get_health_report(self) -> ConfigParserHealthReport:
    return ConfigParserHealthReport(
      healthy=True
    )

  def parse_cpu_config(self, some_data: Any) -> CpuConfig:
    try:
      return from_dict(
        data_class=CpuConfig,
        data=some_data,
        config=Config(
          strict=True
        )
      )
    except Exception as e:
      raise ConfigParserErr(
        config_name="Cpu Config"
      ) from e

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

  def parse_memory_config(self, some_data: Any) -> MemoryConfig:
    try:
      return from_dict(
        data_class=MemoryConfig,
        data=some_data,
        config=Config(
          strict=True
        ),
      )
    except Exception as e:
      raise ConfigParserErr(
        config_name="Memory Config"
      ) from e

  def parse_typicode_config(self, some_data: Any) -> TypicodeConfig:
    try:
      return from_dict(
        data_class=TypicodeConfig,
        data=some_data,
        config=Config(
          strict=True
        ),
      )
    except Exception as e:
      raise ConfigParserErr(
        config_name="Typicode Config"
      ) from e
