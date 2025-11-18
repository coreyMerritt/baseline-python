from dataclasses import dataclass
from typing import List

from shared.enums.logger_level import LoggerLevel
from shared.models.configs.base_config import Config


@dataclass(frozen=True)
class LoggerConfig(Config):
  level: LoggerLevel
  noisy_loggers: List[str]
  timezone: str
