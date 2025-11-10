from dataclasses import dataclass

from infrastructure.models.abc_health_report import HealthReport


@dataclass
class DatabaseHealthReport(HealthReport):
  can_perform_basic_select: bool
  is_engine: bool
  is_logger: bool
  is_not_first_instantiation: bool
  is_session_factory: bool
