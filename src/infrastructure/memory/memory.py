import psutil

from infrastructure.base_infrastructure import BaseInfrastructure
from shared.models.configs.memory_config import MemoryConfig
from shared.models.health_reports.memory_health_report import MemoryHealthReport


class Memory(BaseInfrastructure):
  _memory_config: MemoryConfig

  def __init__(self, memory_config: MemoryConfig):
    self._memory_config = memory_config
    super().__init__()

  def get_health_report(self) -> MemoryHealthReport:
    maximum_healthy_memory_usage_percentage = self._memory_config.maximum_healthy_memory_usage_percentage
    usage_percentage = self.get_memory_usage_percentage()
    healthy = usage_percentage <= maximum_healthy_memory_usage_percentage
    return MemoryHealthReport(
      usage_percentage=usage_percentage,
      healthy=healthy
    )

  def get_memory_usage_percentage(self) -> float:
    return psutil.virtual_memory().percent
