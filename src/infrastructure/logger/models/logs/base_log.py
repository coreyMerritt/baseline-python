from dataclasses import dataclass

from infrastructure.logger.models.logs.log_error import LogError
from infrastructure.logger.models.logs.log_timestamps import LogTimestamps


@dataclass
class BaseLog:
  timestamps: LogTimestamps
  level: str
  message: str
  error: LogError | None

  def __post_init__(self):
    assert type(self) is not BaseLog, "BaseLog is a base class and should not be instantiated"
