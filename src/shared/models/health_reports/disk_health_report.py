from dataclasses import dataclass
from shared.models.health_reports.base_health_report import HealthReport


@dataclass
class DiskHealthReport(HealthReport):
  usage_percentage: float
