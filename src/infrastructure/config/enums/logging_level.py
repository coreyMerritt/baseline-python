from enum import Enum


class LoggingLevel(str, Enum):
  DEBUG = "debug"
  INFO = "info"
  WARNING = "warning"
  ERROR = "error"
  CRITICAL = "critical"
