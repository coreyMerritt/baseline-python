import logging

from infrastructure.logger.enums.logger_level import LoggerLevel
from infrastructure.logger.exceptions.logger_level_err import LoggerLevelErr


class LoggerLevelMapper:
  @staticmethod
  def local_enum_to_logging_const(enum: LoggerLevel) -> int:
    if enum == LoggerLevel.DEBUG:
      return logging.DEBUG
    if enum == LoggerLevel.INFO:
      return logging.INFO
    if enum == LoggerLevel.WARNING:
      return logging.WARNING
    if enum == LoggerLevel.ERROR:
      return logging.ERROR
    if enum == LoggerLevel.CRITICAL:
      return logging.CRITICAL
    raise LoggerLevelErr(f"Bad log level: {enum}")
