import time
from logging import Formatter, LogRecord


class CustomFormatter(Formatter):
  def formatTime(self, record: LogRecord, datefmt: str | None = None) -> str:
    t = time.localtime(record.created)
    return time.strftime("%Y-%m-%d %H:%M:%S", t) + f".{int(record.msecs):03d}"
