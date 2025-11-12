from dataclasses import dataclass
from typing import List

from shared.enums.logger_level import LoggerLevel


@dataclass(frozen=True)
class LoggerConfig:
  level: LoggerLevel
  noisy_loggers: List[str]
