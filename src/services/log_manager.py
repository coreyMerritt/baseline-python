from infrastructure.config.config_manager import ConfigManager
from infrastructure.config.models.logging_config import LoggingConfig
from infrastructure.logging.models.logger_health_report import LoggerHealthReport
from infrastructure.logging.projectname_logger import Logger, ProjectnameLogger
from services.abc_service import Service


class LogManager(Service):
  _is_configured: bool = False
  _logging_config: LoggingConfig

  @staticmethod
  def get_health_report() -> LoggerHealthReport:
    is_configured = LogManager._is_configured
    is_logging_config = LogManager._logging_config is not None
    healthy = is_configured and is_logging_config
    return LoggerHealthReport(
      is_configured=is_configured,
      is_logging_config=is_logging_config,
      healthy=healthy
    )

  @staticmethod
  def get_logger(service_name: str) -> Logger:
    if not LogManager._is_configured:
      LogManager._configure_logger()
    return ProjectnameLogger.get_logger(service_name)

  @staticmethod
  def _configure_logger() -> None:
    if LogManager._is_configured:
      return
    LogManager._logging_config = ConfigManager.get_logging_config()
    ProjectnameLogger.configure_base_logging(LogManager._logging_config.level)
    ProjectnameLogger.inject_custom_formatter()
    noisy_loggers = LogManager._logging_config.noisy_loggers
    if noisy_loggers:
      ProjectnameLogger.silence_noisy_loggers(noisy_loggers)
    LogManager._is_configured = True
