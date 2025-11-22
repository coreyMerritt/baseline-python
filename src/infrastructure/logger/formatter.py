import logging
from datetime import datetime
from zoneinfo import ZoneInfo

from infrastructure.logger.exceptions.formatter_err import FormatterErr


class Formatter(logging.Formatter):
  def __init__(self, fmt: str, timezone: str):
    super().__init__(fmt)
    self.timezone = ZoneInfo(timezone)

  def formatTime(self, record, datefmt=None) -> str:
    if datefmt is not None:
      raise FormatterErr("datefmt should never be overridden")
    dt = datetime.fromtimestamp(record.created, self.timezone)
    # YYYY-MM-DD HH:MM:SS.mmm
    return f"{dt:%Y-%m-%d %H:%M:%S}.{int(record.msecs):03d}"
