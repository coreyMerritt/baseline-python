from dataclasses import dataclass

from shared.models.health_reports.abc_health_report import HealthReport
from shared.models.health_reports.typicode_health_report import TypicodeHealthReport


@dataclass
class ExternalServicesHealthReport(HealthReport):
  typicode_health_report: TypicodeHealthReport
