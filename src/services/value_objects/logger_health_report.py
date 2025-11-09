from dataclasses import dataclass

from services.value_objects.abc_health_report import HealthReport


@dataclass
class LoggerHealthReport(HealthReport):
  configured_is_set: bool
  is_logging_config: bool
