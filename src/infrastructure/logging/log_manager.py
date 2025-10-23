import logging
import time
from typing import List

from infrastructure.config.config_manager import ConfigManager
from infrastructure.config.models.logging_config import LoggingConfig
from infrastructure.logging.exceptions.logger_configuration_exception import LoggerConfigurationException
from infrastructure.logging.exceptions.logger_filter_exception import LoggerFilterException
from infrastructure.logging.filters.service_name_filter import ServiceNameFilter
from infrastructure.logging.mapping.logging_level_mapper import LoggingLevelMapper


class CustomFormatter(logging.Formatter):
  def formatTime(self, record: logging.LogRecord, datefmt: str | None = None) -> str:
    t = time.localtime(record.created)
    return time.strftime("%Y-%m-%d %H:%M:%S", t) + f".{int(record.msecs):03d}"

class LogManager:
  _is_configured: bool = False
  _logging_config: LoggingConfig

  @staticmethod
  def get_logger(service_name: str) -> logging.Logger:
    if not LogManager._is_configured:
      LogManager._configure_logger()
    logger = logging.getLogger(service_name)
    LogManager._add_filters(service_name, logger)
    return logger

  @staticmethod
  def _configure_logger() -> None:
    if LogManager._is_configured:
      return
    LogManager._logging_config = ConfigManager.get_logging_config()
    LogManager._configure_base_logging()
    LogManager._inject_custom_formatter()
    noisy_loggers = LogManager._logging_config.noisy_loggers
    if noisy_loggers:
      LogManager._silence_noisy_loggers(noisy_loggers)
    LogManager._is_configured = True

  @staticmethod
  def _add_filters(service_name: str, logger: logging.Logger) -> None:
    try:
      logger.addFilter(ServiceNameFilter(service_name))
    except Exception as e:
      raise LoggerFilterException() from e

  @staticmethod
  def _configure_base_logging() -> None:
    logging_level_enum = LogManager._logging_config.level
    logging_level_const = LoggingLevelMapper.local_enum_to_logging_const(logging_level_enum)
    try:
      logging.basicConfig(
        format='%(asctime)-25s %(service_name)-20s %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging_level_const
      )
    except Exception as e:
      raise LoggerConfigurationException() from e

  @staticmethod
  def _inject_custom_formatter() -> None:
    for handler in logging.getLogger().handlers:
      handler.setFormatter(CustomFormatter("%(asctime)-25s %(service_name)-20s %(levelname)-8s %(message)s"))

  @staticmethod
  def _silence_noisy_loggers(noisy_loggers: List[str]) -> None:
    try:
      for name in noisy_loggers:
        logging.getLogger(name).setLevel(logging.WARNING)
    except Exception:
      logging.error("Failed to silence noisy loggers: %s", noisy_loggers)

  @staticmethod
  def _custom_time(record: logging.LogRecord) -> str:
    t = time.localtime(record.created)
    return time.strftime("%Y-%m-%d %H:%M:%S", t) + f".{int(record.msecs):03d}"
