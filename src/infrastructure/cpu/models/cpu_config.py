from dataclasses import dataclass


@dataclass(frozen=True)
class CpuConfig():
  cpu_check_interval_seconds: float
  maximum_healthy_cpu_usage_percentage: float
