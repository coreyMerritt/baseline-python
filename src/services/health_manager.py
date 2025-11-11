import json
from dataclasses import asdict

from infrastructure.database.models.database_health_report import DatabaseHealthReport
from infrastructure.logging.models.logger_health_report import LoggerHealthReport
from infrastructure.system_monitoring.models.hardware_util_health_report import HardwareUtilHealthReport
from infrastructure.system_monitoring.system_monitor import SystemMonitor
from services.abc_database_aware_service import DatabaseAwareService
from services.config_manager import ConfigManager
from services.log_manager import LogManager
from services.models.config_health_report import ConfigHealthReport
from services.models.full_health_report import FullHealthReport
from services.models.hardware_util_config import HardwareUtilConfig


class HealthManager(DatabaseAwareService):
  def get_full_health_report(self) -> FullHealthReport:
    health_check_config = ConfigManager.get_health_check_config()
    hardware_util_config = health_check_config.hardware_util
    config_health_report = self.get_config_health_report()
    database_health_report = self.get_database_health_report()
    hardware_util_health_report = self.get_hardware_util_health_report(hardware_util_config)
    logger_health_report = self.get_logger_health_report()
    healthy = (
      config_health_report.healthy
      and database_health_report.healthy
      and hardware_util_health_report.healthy
      and logger_health_report.healthy
    )
    full_health_report = FullHealthReport(
      config_health_report=config_health_report,
      database_health_report=database_health_report,
      hardware_util_health_report=hardware_util_health_report,
      logger_health_report=logger_health_report,
      healthy=healthy
    )
    self._logger.debug("System Health:\n%s", json.dumps(asdict(full_health_report), indent=2))
    return full_health_report

  def get_config_health_report(self) -> ConfigHealthReport:
    return ConfigManager.get_health_report()

  def get_database_health_report(self) -> DatabaseHealthReport:
    return self._database_manager.get_health_report()

  def get_hardware_util_health_report(self, hardware_util_config: HardwareUtilConfig) -> HardwareUtilHealthReport:
    return SystemMonitor.get_health_report(hardware_util_config)

  def get_logger_health_report(self) -> LoggerHealthReport:
    return LogManager.get_health_report()
