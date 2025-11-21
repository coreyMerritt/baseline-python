from dataclasses import dataclass

from shared.models.health_reports.base_health_report import HealthReport


@dataclass
class MemoryHealthReport(HealthReport):
  usage_percentage: float
