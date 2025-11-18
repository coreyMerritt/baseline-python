import psutil

from infrastructure.base_infrastructure import Infrastructure
from shared.models.configs.cpu_config import CpuConfig
from shared.models.health_reports.cpu_health_report import CpuHealthReport


class Cpu(Infrastructure):
  _cpu_config: CpuConfig

  def __init__(self, cpu_config: CpuConfig):
    self._cpu_config = cpu_config

  def get_health_report(self) -> CpuHealthReport:
    maximum_healthy_cpu_usage_percentage = self._cpu_config.maximum_healthy_cpu_usage_percentage
    cpu_usage_percentage = self.get_cpu_usage_percentage()
    healthy = cpu_usage_percentage <= maximum_healthy_cpu_usage_percentage
    return CpuHealthReport(
      healthy=healthy
    )

  def get_cpu_usage_percentage(self) -> float:
    return psutil.cpu_percent(
      interval=self._cpu_config.cpu_check_interval_seconds
    )
