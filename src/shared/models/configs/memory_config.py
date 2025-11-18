from dataclasses import dataclass

from shared.models.configs.base_config import Config

@dataclass(frozen=True)
class MemoryConfig(Config):
  maximum_healthy_memory_usage_percentage: float
