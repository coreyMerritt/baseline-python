import json
from dataclasses import asdict

from infrastructure.external_services.typicode.typicode import Typicode
from infrastructure.system_monitoring.system_monitor import SystemMonitor
from services.abc_database_aware_service import DatabaseAwareService
from shared.models.configs.external_services.external_services_config import ExternalServicesConfig
from shared.models.configs.hardware_util_config import HardwareUtilConfig
from shared.models.configs.health_check_config import HealthCheckConfig
from shared.models.health_reports.database_health_report import DatabaseHealthReport
from shared.models.health_reports.external_services_health_report import ExternalServicesHealthReport
from shared.models.health_reports.full_health_report import FullHealthReport
from shared.models.health_reports.hardware_util_health_report import HardwareUtilHealthReport
from shared.models.health_reports.logger_health_report import LoggerHealthReport


class HealthManager(DatabaseAwareService):
  def get_full_health_report(
    self,
    external_services_config: ExternalServicesConfig,
    health_check_config: HealthCheckConfig
  ) -> FullHealthReport:
    hardware_util_config = health_check_config.hardware_util
    database_health_report = self.get_database_health_report()
    external_services_health_report = self.get_external_services_health_report(external_services_config)
    hardware_util_health_report = self.get_hardware_util_health_report(hardware_util_config)
    logger_health_report = self.get_logger_health_report()
    healthy = (
      database_health_report.healthy
      and external_services_health_report.healthy
      and hardware_util_health_report.healthy
      and logger_health_report.healthy
    )
    full_health_report = FullHealthReport(
      database_health_report=database_health_report,
      external_services_health_report=external_services_health_report,
      hardware_util_health_report=hardware_util_health_report,
      logger_health_report=logger_health_report,
      healthy=healthy
    )
    self._logger.debug("System Health:\n%s", json.dumps(asdict(full_health_report), indent=2))
    return full_health_report

  def get_database_health_report(self) -> DatabaseHealthReport:
    return self._database.get_health_report()

  def get_external_services_health_report(
    self,
    external_services_config: ExternalServicesConfig
  ) -> ExternalServicesHealthReport:
    typicode = Typicode(
      external_services_config.global_,
      external_services_config.typicode
    )
    typicode_health_report = typicode.get_health_report()
    healthy = typicode_health_report.healthy
    return ExternalServicesHealthReport(
      typicode_health_report=typicode_health_report,
      healthy=healthy
    )

  def get_hardware_util_health_report(self, hardware_util_config: HardwareUtilConfig) -> HardwareUtilHealthReport:
    return SystemMonitor.get_health_report(hardware_util_config)

  def get_logger_health_report(self) -> LoggerHealthReport:
    return self._logger.get_health_report()
