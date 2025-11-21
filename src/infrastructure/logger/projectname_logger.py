import logging

from infrastructure.base_infrastructure import BaseInfrastructure
from infrastructure.logger.exceptions.logger_configuration_err import LoggerConfigurationErr
from infrastructure.logger.exceptions.logger_initialization_err import LoggerInitializationErr
from infrastructure.logger.formatters.projectname_logger_formatter import CustomFormatter
from infrastructure.logger.mapping.logger_level_mapper import LoggerLevelMapper
from shared.models.configs.logger_config import LoggerConfig
from shared.models.health_reports.logger_health_report import LoggerHealthReport


class ProjectnameLogger(BaseInfrastructure):
  _is_configured: bool = False

  def __init__(self, logger_config: LoggerConfig):
    try:
      if not self._is_configured:
        self._configure_logger(logger_config)
      self._logger = logging.getLogger("Projectname Logger")
      super().__init__()
    except Exception as e:
      raise LoggerInitializationErr() from e

  def get_health_report(self) -> LoggerHealthReport:
    is_configured = self._is_configured
    healthy = is_configured
    return LoggerHealthReport(
      is_configured=is_configured,
      healthy=healthy
    )

  def _configure_logger(self, logger_config: LoggerConfig) -> None:
    try:
      if self._is_configured:
        return
      level = LoggerLevelMapper.local_enum_to_logging_const(logger_config.level)
      logging.basicConfig(level=level)
      for handler in logging.getLogger().handlers:
        handler.setFormatter(CustomFormatter("%(asctime)-24s %(levelname)-9s %(message)s"))
      for name in logger_config.noisy_loggers or []:
        logging.getLogger(name).setLevel(logging.WARNING)
      self._is_configured = True
    except Exception as e:
      raise LoggerConfigurationErr() from e

  def debug(self, *args, **kwargs) -> None:
    return self._logger.debug(*args, **kwargs)

  def info(self, *args, **kwargs) -> None:
    return self._logger.info(*args, **kwargs)

  def warning(self, *args, **kwargs) -> None:
    return self._logger.warning(*args, **kwargs)

  def error(self, *args, **kwargs) -> None:
    return self._logger.error(*args, **kwargs)

  def critical(self, *args, **kwargs) -> None:
    return self._logger.critical(*args, **kwargs)
