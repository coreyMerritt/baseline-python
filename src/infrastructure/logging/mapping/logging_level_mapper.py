import logging

from infrastructure.config.enums.logging_level import LoggingLevel
from infrastructure.logging.exceptions.logger_level_exception import LoggerLevelException


class LoggingLevelMapper:
  @staticmethod
  def local_enum_to_logging_const(enum: LoggingLevel) -> int:
    if enum == LoggingLevel.DEBUG:
      return logging.DEBUG
    elif enum == LoggingLevel.INFO:
      return logging.INFO
    elif enum == LoggingLevel.WARNING:
      return logging.WARNING
    elif enum == LoggingLevel.ERROR:
      return logging.ERROR
    elif enum == LoggingLevel.CRITICAL:
      return logging.CRITICAL
    else:
      raise LoggerLevelException(f"Bad log level: {enum}")
