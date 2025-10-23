from dataclasses import dataclass
from typing import List

from infrastructure.config.enums.logging_level import LoggingLevel


@dataclass(frozen=True)
class LoggingConfig:
  level: LoggingLevel
  noisy_loggers: List[str]
