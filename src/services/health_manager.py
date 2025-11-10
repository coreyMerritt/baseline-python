from infrastructure.config.config_manager import ConfigManager
from infrastructure.config.models.hardware_util_config import HardwareUtilConfig
from infrastructure.logging.log_manager import LogManager
from infrastructure.system_monitoring.system_monitor import SystemMonitor
from services.abc_service import Service
from services.value_objects.config_health_report import ConfigHealthReport
from services.value_objects.database_health_report import DatabaseHealthReport
from services.value_objects.full_health_report import FullHealthReport
from services.value_objects.hardware_util_health_report import HardwareUtilHealthReport
from services.value_objects.logger_health_report import LoggerHealthReport


class HealthManager(Service):
  def get_full_health_report(self) -> FullHealthReport:
    health_check_config = ConfigManager.get_health_check_config()
    hardware_util_config = health_check_config.hardware_util
    config_health_report = self.get_config_health_report()
    database_health_report = self.get_database_health_report()
    hardware_util_health_report = self.get_hardware_util_health_report(hardware_util_config)
    logger_health_report = self.get_logger_health_report()
    healthy = (
      config_health_report.healthy
      and database_health_report.healthy
      and hardware_util_health_report.healthy
      and logger_health_report.healthy
    )
    return FullHealthReport(
      config_health_report=config_health_report,
      database_health_report=database_health_report,
      hardware_util_health_report=hardware_util_health_report,
      logger_health_report=logger_health_report,
      healthy=healthy
    )

  def get_config_health_report(self) -> ConfigHealthReport:
    is_config_dir = ConfigManager.is_config_dir()
    is_configured = ConfigManager.is_configured()
    is_database_config = ConfigManager.is_database_config()
    is_environment = ConfigManager.is_environment()
    is_health_check_config = ConfigManager.is_health_check_config()
    is_logging_config = ConfigManager.is_logging_config()
    healthy = (
      is_config_dir
      and is_configured
      and is_database_config
      and is_environment
      and is_health_check_config
      and is_logging_config
    )
    return ConfigHealthReport(
      is_config_dir=is_config_dir,
      is_configured=is_configured,
      is_database_config=is_database_config,
      is_environment=is_environment,
      is_health_check_config=is_health_check_config,
      is_logging_config=is_logging_config,
      healthy=healthy
    )

  def get_database_health_report(self) -> DatabaseHealthReport:
    can_perform_basic_select = self._database_manager.can_perform_basic_select()
    is_not_first_instantiation = not self._database_manager.is_first_instantiation()
    is_engine = self._database_manager.is_engine()
    is_logger = self._database_manager.is_logger()
    is_session_factory = self._database_manager.is_session_factory()
    healthy = can_perform_basic_select and is_not_first_instantiation and is_engine and is_logger and is_session_factory
    return DatabaseHealthReport(
      can_perform_basic_select=can_perform_basic_select,
      is_engine=is_engine,
      is_logger=is_logger,
      is_not_first_instantiation=is_not_first_instantiation,
      is_session_factory=is_session_factory,
      healthy=healthy
    )

  def get_hardware_util_health_report(self, hardware_util_config: HardwareUtilConfig) -> HardwareUtilHealthReport:
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

  def get_logger_health_report(self) -> LoggerHealthReport:
    is_configured = LogManager.is_configured()
    is_logging_config = LogManager.is_logging_config()
    healthy = is_configured and is_logging_config
    return LoggerHealthReport(
      is_configured=is_configured,
      is_logging_config=is_logging_config,
      healthy=healthy
    )
