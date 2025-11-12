from dataclasses import dataclass

from shared.models.health_reports.abc_health_report import HealthReport


@dataclass
class ExternalServicesHealthReport(HealthReport):
  is_external_services_config: bool
