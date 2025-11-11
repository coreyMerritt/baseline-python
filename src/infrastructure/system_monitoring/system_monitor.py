import psutil

from infrastructure.abc_infrastructure import Infrastructure
from infrastructure.system_monitoring.models.hardware_util_health_report import HardwareUtilHealthReport
from services.models.hardware_util_config import HardwareUtilConfig


class SystemMonitor(Infrastructure):
  @staticmethod
  def get_health_report(hardware_util_config: HardwareUtilConfig) -> HardwareUtilHealthReport:
    cpu_check_interval_seconds = hardware_util_config.cpu_check_interval_seconds
    maximum_healthy_cpu_usage_percentage = hardware_util_config.maximum_healthy_cpu_usage_percentage
    maximum_healthy_disk_usage_percentage = hardware_util_config.maximum_healthy_disk_usage_percentage
    maximum_healthy_memory_usage_percentage = hardware_util_config.maximum_healthy_memory_usage_percentage
    system_monitor = SystemMonitor()
    cpu_usage_percentage = system_monitor.get_cpu_usage_percentage(cpu_check_interval_seconds)
    disk_usage_percentage = system_monitor.get_disk_usage_percentage()
    memory_usage_percentage = system_monitor.get_memory_usage_percentage()
    cpu_healthy = cpu_usage_percentage <= maximum_healthy_cpu_usage_percentage
    disk_healthy = disk_usage_percentage <= maximum_healthy_disk_usage_percentage
    memory_healthy = memory_usage_percentage <= maximum_healthy_memory_usage_percentage
    healthy = cpu_healthy and disk_healthy and memory_healthy
    return HardwareUtilHealthReport(
      cpu_healthy=cpu_healthy,
      disk_healthy=disk_healthy,
      memory_healthy=memory_healthy,
      healthy=healthy
    )

  @staticmethod
  def get_cpu_usage_percentage(cpu_check_interval_seconds: float) -> float:
    return psutil.cpu_percent(interval=cpu_check_interval_seconds)

  @staticmethod
  def get_disk_usage_percentage() -> float:
    return psutil.disk_usage("/").percent

  @staticmethod
  def get_memory_usage_percentage() -> float:
    return psutil.virtual_memory().percent
