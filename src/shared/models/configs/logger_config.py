from dataclasses import dataclass
from typing import List

from shared.models.configs.base_config import Config
from shared.enums.logger_level import LoggerLevel


@dataclass(frozen=True)
class LoggerConfig(Config):
  level: LoggerLevel
  noisy_loggers: List[str]
  timezone: str
