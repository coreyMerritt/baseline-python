from dataclasses import dataclass

from shared.models.health_reports.base_health_report import HealthReport


@dataclass
class LoggerHealthReport(HealthReport):
  is_configured: bool
