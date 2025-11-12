from dataclasses import dataclass

from shared.models.configs.hardware_util_config import HardwareUtilConfig


@dataclass(frozen=True)
class HealthCheckConfig:
  hardware_util: HardwareUtilConfig
