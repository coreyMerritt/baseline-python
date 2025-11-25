import json
import traceback
from dataclasses import asdict
from datetime import datetime
from zoneinfo import ZoneInfo

from rich.traceback import install as install_rich_tracebacks

from infrastructure.logger.enums.logger_level import LoggerLevel
from infrastructure.logger.exceptions.logger_initialization_err import LoggerInitializationErr
from infrastructure.logger.models.logger_config import LoggerConfig
from infrastructure.logger.models.logger_health_report import LoggerHealthReport
from infrastructure.logger.models.logs.base_log import BaseLog
from infrastructure.logger.models.logs.http_log import HTTPLog
from infrastructure.logger.models.logs.log_error import LogError
from infrastructure.logger.models.logs.log_ids import LogIDs
from infrastructure.logger.models.logs.log_timestamps import LogTimestamps
from infrastructure.logger.models.logs.simple_log import SimpleLog
from infrastructure.types.logger_interface import LoggerInterface
from shared.enums.deployment_environment import DeploymentEnvironment
from shared.exceptions.undocumented_case_err import UndocumentedCaseErr


class ProjectnameLogger(LoggerInterface):
  _deployment_environment: DeploymentEnvironment
  _level: LoggerLevel
  _zoneinfo: ZoneInfo

  def __init__(self, deployment_environment: DeploymentEnvironment, logger_config: LoggerConfig):
    try:
      install_rich_tracebacks()
      self._deployment_environment = deployment_environment
      self._level = logger_config.level
      self._zoneinfo = ZoneInfo(logger_config.timezone.value)
      super().__init__()
    except Exception as e:
      raise LoggerInitializationErr() from e

  def get_health_report(self) -> LoggerHealthReport:
    return LoggerHealthReport(
      healthy=True
    )

  def debug(
    self,
    message: str,
    correlation_id: str | None = None,
    endpoint: str | None = None,
    request_id: str | None = None
  ) -> None:
    if self._level not in (
      LoggerLevel.DEBUG
    ):
      return
    level = "DEBUG"
    log = self._get_some_log(message, level, None, correlation_id, endpoint, request_id)
    self._print_log(log, None)

  def info(
    self,
    message: str,
    correlation_id: str | None = None,
    endpoint: str | None = None,
    request_id: str | None = None
  ) -> None:
    if self._level not in (
      LoggerLevel.INFO,
      LoggerLevel.DEBUG
    ):
      return
    level = "INFO"
    log = self._get_some_log(message, level, None, correlation_id, endpoint, request_id)
    self._print_log(log, None)

  def warning(
    self,
    message: str,
    error: Exception | None = None,
    correlation_id: str | None = None,
    endpoint: str | None = None,
    request_id: str | None = None
  ) -> None:
    if self._level not in (
      LoggerLevel.WARNING,
      LoggerLevel.INFO,
      LoggerLevel.DEBUG
    ):
      return
    level = "WARNING"
    log = self._get_some_log(message, level, error, correlation_id, endpoint, request_id)
    self._print_log(log, error)

  def err(
    self,
    message: str,
    error: Exception,
    correlation_id: str | None = None,
    endpoint: str | None = None,
    request_id: str | None = None
  ) -> None:
    if self._level not in (
      LoggerLevel.ERROR,
      LoggerLevel.WARNING,
      LoggerLevel.INFO,
      LoggerLevel.DEBUG
    ):
      return
    level = "ERROR"
    log = self._get_some_log(message, level, error, correlation_id, endpoint, request_id)
    self._print_log(log, error)

  def critical(
    self,
    message: str,
    error: Exception,
    correlation_id: str | None = None,
    endpoint: str | None = None,
    request_id: str | None = None
  ) -> None:
    if self._level not in (
      LoggerLevel.CRITICAL,
      LoggerLevel.ERROR,
      LoggerLevel.WARNING,
      LoggerLevel.INFO,
      LoggerLevel.DEBUG
    ):
      return
    level = "CRITICAL"
    log = self._get_some_log(message, level, error, correlation_id, endpoint, request_id)
    self._print_log(log, error)

  def _get_some_log(
    self,
    message: str,
    level: str,
    error: Exception | None,
    correlation_id: str | None,
    endpoint: str | None,
    request_id: str | None
  ) -> BaseLog:
    log: BaseLog
    if correlation_id and endpoint and request_id:
      log = self._get_http_log(message, level, error, correlation_id, endpoint, request_id)
    else:
      log = self._get_simple_log(message, level, error)
    return log

  def _get_simple_log(self, message: str, level: str, error: Exception | None) -> SimpleLog:
    timestamps = self._get_log_timestamps()
    log_error = self._get_log_error(error)
    return SimpleLog(
      timestamps=timestamps,
      level=level,
      message=message,
      error=log_error
    )

  def _get_http_log(
    self,
    message: str,
    level: str,
    error: Exception | None,
    correlation_id: str,
    endpoint: str,
    request_id: str
  ) -> HTTPLog:
    timestamps = self._get_log_timestamps()
    log_error = self._get_log_error(error)
    log_ids = self._get_log_ids(correlation_id, request_id)
    return HTTPLog(
      timestamps=timestamps,
      level=level,
      message=message,
      error=log_error,
      ids=log_ids,
      endpoint=endpoint
    )

  def _get_log_ids(self, correlation_id: str, request_id: str) -> LogIDs:
    return LogIDs(
      correlation_id=correlation_id,
      request_id=request_id
    )

  def _get_log_timestamps(self) -> LogTimestamps:
    now = datetime.now(self._zoneinfo)
    human_timestamp = self._get_human_timestamp(now)
    machine_timestamp = self._get_machine_timestamp(now)
    return LogTimestamps(
      human=human_timestamp,
      machine=machine_timestamp
    )

  def _get_log_error(self, exception: Exception | None) -> LogError | None:
    if not exception:
      return None
    return LogError(
      name=type(exception).__name__,
      message=str(exception),
      stack="".join(traceback.format_exception(exception)).replace("\n", "\\n")
    )

  def _get_human_timestamp(self, now: datetime) -> str:
    return now.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(now.microsecond / 1000):03d}"

  def _get_machine_timestamp(self, now: datetime) -> str:
    return now.isoformat()

  def _print_log(self, log: BaseLog, err: Exception | None) -> None:
    if self._deployment_environment == DeploymentEnvironment.DEV:
      self._print_human_readable_log(log, err)
    elif self._deployment_environment == DeploymentEnvironment.PROD:
      print(json.dumps(asdict(log), indent=2))
    elif self._deployment_environment == DeploymentEnvironment.TEST:
      print(json.dumps(asdict(log), indent=2))
    else:
      raise UndocumentedCaseErr()

  def _print_human_readable_log(self, log: BaseLog, err: Exception | None) -> None:
    if isinstance(log, SimpleLog):
      self._print_human_readable_simple_log(log, err)
    elif isinstance(log, HTTPLog):
      self._print_human_readable_http_log(log, err)
    else:
      raise UndocumentedCaseErr()

  def _print_human_readable_simple_log(self, simple_log: SimpleLog, err: Exception | None) -> None:
    print(f"     Timestamp: {simple_log.timestamps.human}")
    print(f"         Level: {simple_log.level}")
    print(f"       Message: {simple_log.message}")
    if err:
      print()
      traceback.print_exception(type(err), err, err.__traceback__)
    print("─" * 120)

  def _print_human_readable_http_log(self, http_log: HTTPLog, err: Exception | None) -> None:
    print(f"     Timestamp: {http_log.timestamps.human}")
    print(f"         Level: {http_log.level}")
    print(f"       Message: {http_log.message}")
    print(f"    Request ID: {http_log.ids.request_id}")
    print(f"Correlation ID: {http_log.ids.correlation_id}")
    print(f"      Endpoint: {http_log.endpoint}")
    if err:
      print()
      traceback.print_exception(type(err), err, err.__traceback__)
    print("─" * 120)
