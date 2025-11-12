from infrastructure.logger.projectname_logger import Logger, ProjectnameLogger
from services.abc_service import Service
from services.config_manager import ConfigManager
from shared.models.configs.logger_config import LoggerConfig
from shared.models.health_reports.logger_health_report import LoggerHealthReport


class LogManager(Service):
  _is_configured: bool = False
  _logger_config: LoggerConfig

  @staticmethod
  def get_health_report() -> LoggerHealthReport:
    is_configured = LogManager._is_configured
    is_logger_config = LogManager._logger_config is not None
    healthy = is_configured and is_logger_config
    return LoggerHealthReport(
      is_configured=is_configured,
      is_logger_config=is_logger_config,
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
    LogManager._logger_config = ConfigManager.get_logger_config()
    ProjectnameLogger.configure_base_logging(LogManager._logger_config.level)
    ProjectnameLogger.inject_custom_formatter()
    noisy_loggers = LogManager._logger_config.noisy_loggers
    if noisy_loggers:
      ProjectnameLogger.silence_noisy_loggers(noisy_loggers)
    LogManager._is_configured = True
