from dataclasses import dataclass

from shared.models.health_reports.abc_health_report import HealthReport


@dataclass
class HardwareUtilHealthReport(HealthReport):
  cpu_healthy: bool
  disk_healthy: bool
  memory_healthy: bool
