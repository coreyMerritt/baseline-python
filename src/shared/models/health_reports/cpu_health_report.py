from dataclasses import dataclass

from shared.models.health_reports.abc_health_report import HealthReport


@dataclass
class CpuHealthReport(HealthReport):
  """ Only returns base health report values """
