from dataclasses import dataclass

from infrastructure.models.abc_health_report import HealthReport


@dataclass
class TypicodeHealthReport(HealthReport):
  is_external_global_config: bool
  is_typicode_config: bool
