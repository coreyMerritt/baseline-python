from dataclasses import dataclass


@dataclass(frozen=True)
class HardwareUtilConfig:
  cpu_check_interval_seconds: float
  maximum_healthy_cpu_usage_percentage: float
  maximum_healthy_disk_usage_percentage: float
  maximum_healthy_memory_usage_percentage: float
