from dataclasses import dataclass, field

from shared.models.health_reports.config_parser_health_report import ConfigParserHealthReport
from shared.models.health_reports.cpu_health_report import CpuHealthReport
from shared.models.health_reports.database_health_report import DatabaseHealthReport
from shared.models.health_reports.disk_health_report import DiskHealthReport
from shared.models.health_reports.environment_health_report import EnvironmentHealthReport
from shared.models.health_reports.logger_health_report import LoggerHealthReport
from shared.models.health_reports.memory_health_report import MemoryHealthReport
from shared.models.health_reports.typicode_health_report import TypicodeHealthReport


@dataclass
class FullHealthReport():
  healthy: bool = field(init=False)
  config_parser_health_report: ConfigParserHealthReport
  cpu_health_report: CpuHealthReport
  database_health_report: DatabaseHealthReport
  disk_health_report: DiskHealthReport
  environment_health_report: EnvironmentHealthReport
  logger_health_report: LoggerHealthReport
  memory_health_report: MemoryHealthReport
  typicode_health_report: TypicodeHealthReport

  def __post_init__(self):
    self.healthy = (
      self.config_parser_health_report.healthy
      and self.cpu_health_report.healthy
      and self.database_health_report.healthy
      and self.disk_health_report.healthy
      and self.environment_health_report.healthy
      and self.logger_health_report.healthy
      and self.memory_health_report.healthy
      and self.typicode_health_report.healthy
    )
