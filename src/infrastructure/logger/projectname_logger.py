from logging import WARNING, Logger, basicConfig, error, getLogger
from typing import List

from infrastructure.abc_infrastructure import Infrastructure
from infrastructure.logger.exceptions.logger_configuration_err import LoggerConfigurationErr
from infrastructure.logger.formatters.projectname_logger_formatter import CustomFormatter
from infrastructure.logger.mapping.logger_level_mapper import LoggerLevelMapper
from shared.enums.logger_level import LoggerLevel
from shared.models.configs.logger_config import LoggerConfig
from shared.models.health_reports.logger_health_report import LoggerHealthReport


class ProjectnameLogger(Infrastructure, Logger):
  _is_configured: bool = False

  def __init__(self, logger_config: LoggerConfig):
    if not self._is_configured:
      self._configure_logger(logger_config)
    super().__init__("Projectname Logger")

  def get_health_report(self) -> LoggerHealthReport:
    is_configured = self._is_configured
    healthy = is_configured
    return LoggerHealthReport(
      is_configured=is_configured,
      healthy=healthy
    )

  def _configure_logger(self, logger_config: LoggerConfig) -> None:
    if self._is_configured:
      return
    self._configure_base_logging(logger_config.level)
    self._inject_custom_formatter()
    noisy_loggers = logger_config.noisy_loggers
    if noisy_loggers:
      self._silence_noisy_loggers(noisy_loggers)
    self._is_configured = True

  def _configure_base_logging(self, logger_level_enum: LoggerLevel) -> None:
    logging_level_const = LoggerLevelMapper.local_enum_to_logging_const(logger_level_enum)
    try:
      basicConfig(
        level=logging_level_const
      )
    except Exception as e:
      raise LoggerConfigurationErr() from e

  def _inject_custom_formatter(self) -> None:
    for handler in getLogger().handlers:
      handler.setFormatter(CustomFormatter("%(asctime)-24s %(levelname)-9s %(message)s"))

  def _silence_noisy_loggers(self, noisy_loggers: List[str]) -> None:
    try:
      for name in noisy_loggers:
        getLogger(name).setLevel(WARNING)
    except Exception:
      error("Failed to silence noisy loggers: %s", noisy_loggers)
