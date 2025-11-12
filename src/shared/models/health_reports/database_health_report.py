from dataclasses import dataclass

from shared.models.health_reports.abc_health_report import HealthReport


@dataclass
class DatabaseHealthReport(HealthReport):
  can_perform_basic_select: bool
  is_engine: bool
  is_session_factory: bool
