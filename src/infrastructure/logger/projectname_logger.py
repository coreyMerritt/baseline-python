import time
from logging import WARNING, Formatter, Logger, LogRecord, basicConfig, error, getLogger
from typing import List

from infrastructure.abc_infrastructure import Infrastructure
from infrastructure.logger.exceptions.logger_configuration_err import LoggerConfigurationErr
from infrastructure.logger.mapping.logger_level_mapper import LoggerLevelMapper
from shared.enums.logger_level import LoggerLevel


class CustomFormatter(Formatter):
  def formatTime(self, record: LogRecord, datefmt: str | None = None) -> str:
    t = time.localtime(record.created)
    return time.strftime("%Y-%m-%d %H:%M:%S", t) + f".{int(record.msecs):03d}"


class ProjectnameLogger(Infrastructure):
  @staticmethod
  def get_logger(service_name: str) -> Logger:
    logger = getLogger(service_name)
    return logger

  @staticmethod
  def configure_base_logging(logger_level_enum: LoggerLevel) -> None:
    logging_level_const = LoggerLevelMapper.local_enum_to_logging_const(logger_level_enum)
    try:
      basicConfig(
        level=logging_level_const
      )
    except Exception as e:
      raise LoggerConfigurationErr(str(e)) from e

  @staticmethod
  def inject_custom_formatter() -> None:
    for handler in getLogger().handlers:
      handler.setFormatter(CustomFormatter("%(asctime)-24s %(levelname)-9s %(message)s"))

  @staticmethod
  def silence_noisy_loggers(noisy_loggers: List[str]) -> None:
    try:
      for name in noisy_loggers:
        getLogger(name).setLevel(WARNING)
    except Exception:
      error("Failed to silence noisy loggers: %s", noisy_loggers)
