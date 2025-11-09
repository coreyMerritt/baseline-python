from dataclasses import dataclass

from infrastructure.config.models.hardware_util_config import HardwareUtilConfig


@dataclass(frozen=True)
class HealthCheckConfig:
  hardware_util: HardwareUtilConfig
