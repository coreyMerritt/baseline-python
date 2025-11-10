from dataclasses import dataclass

from infrastructure.models.abc_health_report import HealthReport


@dataclass
class ConfigHealthReport(HealthReport):
  is_config_dir: bool
  is_configured: bool
  is_database_config: bool
  is_health_check_config: bool
  is_environment: bool
  is_logging_config: bool
