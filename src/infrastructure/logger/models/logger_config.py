from dataclasses import dataclass

from infrastructure.logger.enums.logger_level import LoggerLevel
from shared.enums.timezone import Timezone


@dataclass(frozen=True)
class LoggerConfig():
  level: LoggerLevel
  timezone: Timezone
