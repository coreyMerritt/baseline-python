from dataclasses import dataclass

from shared.models.configs.base_config import Config

@dataclass(frozen=True)
class DiskConfig(Config):
  maximum_healthy_disk_usage_percentage: float
