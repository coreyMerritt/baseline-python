from dataclasses import dataclass

from shared.models.configs.base_config import Config

@dataclass(frozen=True)
class CpuConfig(Config):
  cpu_check_interval_seconds: float
  maximum_healthy_cpu_usage_percentage: float
