import psutil

from infrastructure.base_infrastructure import Infrastructure
from shared.models.configs.memory_config import MemoryConfig
from shared.models.health_reports.memory_health_report import MemoryHealthReport


class Memory(Infrastructure):
  _memory_config: MemoryConfig

  def __init__(self, memory_config: MemoryConfig):
    self._memory_config = memory_config
    super().__init__()

  def get_health_report(self) -> MemoryHealthReport:
    maximum_healthy_memory_usage_percentage = self._memory_config.maximum_healthy_memory_usage_percentage
    memory_usage_percentage = self.get_memory_usage_percentage()
    healthy = memory_usage_percentage <= maximum_healthy_memory_usage_percentage
    return MemoryHealthReport(
      healthy=healthy
    )

  def get_memory_usage_percentage(self) -> float:
    return psutil.virtual_memory().percent
