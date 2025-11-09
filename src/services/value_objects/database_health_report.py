from dataclasses import dataclass

from services.value_objects.abc_health_report import HealthReport


@dataclass
class DatabaseHealthReport(HealthReport):
  can_perform_basic_select: bool
  first_instantiation_is_set: bool
  is_engine: bool
  is_logger: bool
  is_session_factory: bool
