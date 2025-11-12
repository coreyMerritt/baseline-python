from dataclasses import dataclass

from shared.models.health_reports.abc_health_report import HealthReport
from shared.models.health_reports.config_health_report import ConfigHealthReport
from shared.models.health_reports.database_health_report import DatabaseHealthReport
from shared.models.health_reports.hardware_util_health_report import HardwareUtilHealthReport
from shared.models.health_reports.logger_health_report import LoggerHealthReport


@dataclass
class FullHealthReport(HealthReport):
  config_health_report: ConfigHealthReport
  database_health_report: DatabaseHealthReport
  hardware_util_health_report: HardwareUtilHealthReport
  logger_health_report: LoggerHealthReport
