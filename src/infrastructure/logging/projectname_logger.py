from logging import Formatter, Logger, LogRecord, basicConfig, error, getLogger, WARNING
import time
from typing import List

from infrastructure.abc_infrastructure import Infrastructure
from infrastructure.config.config_manager import ConfigManager
from infrastructure.config.models.logging_config import LoggingConfig
from infrastructure.logging.exceptions.logger_configuration_exception import LoggerConfigurationException
from infrastructure.logging.mapping.logging_level_mapper import LoggingLevelMapper
from infrastructure.logging.models.logger_health_report import LoggerHealthReport


class CustomFormatter(Formatter):
  def formatTime(self, record: LogRecord, datefmt: str | None = None) -> str:
    t = time.localtime(record.created)
    return time.strftime("%Y-%m-%d %H:%M:%S", t) + f".{int(record.msecs):03d}"


class ProjectnameLogger(Infrastructure):
  _is_configured: bool = False
  _logging_config: LoggingConfig

  @staticmethod
  def get_health_report() -> LoggerHealthReport:
    is_configured = ProjectnameLogger.is_configured()
    is_logging_config = ProjectnameLogger.is_logging_config()
    healthy = is_configured and is_logging_config
    return LoggerHealthReport(
      is_configured=is_configured,
      is_logging_config=is_logging_config,
      healthy=healthy
    )

  @staticmethod
  def is_configured() -> bool:
    return ProjectnameLogger._is_configured

  @staticmethod
  def is_logging_config() -> bool:
    return ProjectnameLogger._logging_config is not None

  @staticmethod
  def get_logger(service_name: str) -> Logger:
    if not ProjectnameLogger._is_configured:
      ProjectnameLogger._configure_logger()
    logger = getLogger(service_name)
    return logger

  @staticmethod
  def _configure_logger() -> None:
    if ProjectnameLogger._is_configured:
      return
    ProjectnameLogger._logging_config = ConfigManager.get_logging_config()
    ProjectnameLogger._configure_base_logging()
    ProjectnameLogger._inject_custom_formatter()
    noisy_loggers = ProjectnameLogger._logging_config.noisy_loggers
    if noisy_loggers:
      ProjectnameLogger._silence_noisy_loggers(noisy_loggers)
    ProjectnameLogger._is_configured = True

  @staticmethod
  def _configure_base_logging() -> None:
    logging_level_enum = ProjectnameLogger._logging_config.level
    logging_level_const = LoggingLevelMapper.local_enum_to_logging_const(logging_level_enum)
    try:
      basicConfig(
        level=logging_level_const
      )
    except Exception as e:
      raise LoggerConfigurationException(str(e)) from e

  @staticmethod
  def _inject_custom_formatter() -> None:
    for handler in getLogger().handlers:
      handler.setFormatter(CustomFormatter("%(asctime)-24s %(levelname)-9s %(message)s"))

  @staticmethod
  def _silence_noisy_loggers(noisy_loggers: List[str]) -> None:
    try:
      for name in noisy_loggers:
        getLogger(name).setLevel(WARNING)
    except Exception:
      error("Failed to silence noisy loggers: %s", noisy_loggers)
