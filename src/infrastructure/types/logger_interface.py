from typing import Protocol

from infrastructure.logger.models.logger_health_report import LoggerHealthReport


class LoggerInterface(Protocol):
  def get_health_report(self) -> LoggerHealthReport: ...
  def debug(
    self,
    message: str,
    correlation_id: str | None = None,
    endpoint: str | None = None,
    request_id: str | None = None
  ) -> None: ...
  def info(
    self,
    message: str,
    correlation_id: str | None = None,
    endpoint: str | None = None,
    request_id: str | None = None
  ) -> None: ...
  def warning(
    self,
    message: str,
    error: Exception | None = None,
    correlation_id: str | None = None,
    endpoint: str | None = None,
    request_id: str | None = None
  ) -> None: ...
  def err(
    self,
    message: str,
    error: Exception,
    correlation_id: str | None = None,
    endpoint: str | None = None,
    request_id: str | None = None
  ) -> None: ...
  def critical(
    self,
    message: str,
    error: Exception,
    correlation_id: str | None = None,
    endpoint: str | None = None,
    request_id: str | None = None
  ) -> None: ...
