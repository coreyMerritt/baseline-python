from dataclasses import dataclass

from shared.models.configs.base_config import Config
from shared.models.configs.hardware_util_config import HardwareUtilConfig


@dataclass(frozen=True)
class HealthCheckConfig(Config):
  hardware_util: HardwareUtilConfig
