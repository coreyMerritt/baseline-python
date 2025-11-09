import psutil


class SystemMonitor:
  @staticmethod
  def get_cpu_usage_percentage(cpu_check_interval_seconds: float) -> float:
    return psutil.cpu_percent(interval=cpu_check_interval_seconds)

  @staticmethod
  def get_disk_usage_percentage() -> float:
    return psutil.disk_usage("/").percent

  @staticmethod
  def get_memory_usage_percentage() -> float:
    return psutil.virtual_memory().percent
