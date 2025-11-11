from dataclasses import dataclass

from services.models.hardware_util_config import HardwareUtilConfig


@dataclass(frozen=True)
class HealthCheckConfig:
  hardware_util: HardwareUtilConfig
