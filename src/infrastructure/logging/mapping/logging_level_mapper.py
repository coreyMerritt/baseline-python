import logging

from infrastructure.logging.exceptions.logger_level_exception import LoggerLevelException
from services.enums.logging_level import LoggingLevel


class LoggingLevelMapper:
  @staticmethod
  def local_enum_to_logging_const(enum: LoggingLevel) -> int:
    if enum == LoggingLevel.DEBUG:
      return logging.DEBUG
    if enum == LoggingLevel.INFO:
      return logging.INFO
    if enum == LoggingLevel.WARNING:
      return logging.WARNING
    if enum == LoggingLevel.ERROR:
      return logging.ERROR
    if enum == LoggingLevel.CRITICAL:
      return logging.CRITICAL
    raise LoggerLevelException(f"Bad log level: {enum}")
