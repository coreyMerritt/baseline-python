from dataclasses import dataclass
from typing import List

from infrastructure.enums.timezone import Timezone
from infrastructure.logger.enums.logger_level import LoggerLevel


@dataclass(frozen=True)
class LoggerConfig():
  level: LoggerLevel
  noisy_loggers: List[str]
  timezone: Timezone
