from dataclasses import dataclass

from shared.models.health_reports.abc_health_report import HealthReport


@dataclass
class ConfigHealthReport(HealthReport):
  is_config_dir: bool
  is_configured: bool
  is_database_config: bool
  is_external_services_config: bool
  is_health_check_config: bool
  is_logger_config: bool
