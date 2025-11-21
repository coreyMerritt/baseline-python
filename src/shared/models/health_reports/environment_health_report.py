from dataclasses import dataclass

from shared.models.health_reports.base_health_report import HealthReport


@dataclass
class EnvironmentHealthReport(HealthReport):
  """ Only contains base health report values """
