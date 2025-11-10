from dataclasses import dataclass

from infrastructure.models.abc_health_report import HealthReport


@dataclass
class LoggerHealthReport(HealthReport):
  is_configured: bool
  is_logging_config: bool
