from interfaces.rest.health.adapters.get_config_health_report_adapter import GetConfigHealthReportAdapter
from interfaces.rest.health.adapters.get_database_health_report_adapter import GetDatabaseHealthReportAdapter
from interfaces.rest.health.adapters.get_hardware_util_health_report_adapter import GetHardwareUtilHealthReportAdapter
from interfaces.rest.health.adapters.get_logger_health_report_adapter import GetLoggerHealthReportAdapter
from interfaces.rest.health.dto.res.get_full_health_report_res import GetFullHealthReportRes
from interfaces.rest.health.exceptions.health_adapter_exception import HealthAdapterException
from services.value_objects.full_health_report import FullHealthReport


class GetFullHealthReportAdapter:
  @staticmethod
  def valueobject_to_res(value_object: FullHealthReport) -> GetFullHealthReportRes:
    config_health_report = GetConfigHealthReportAdapter.valueobject_to_res(
      value_object.config_health_report
    )
    database_health_report = GetDatabaseHealthReportAdapter.valueobject_to_res(
      value_object.database_health_report
    )
    hardware_util_health_report = GetHardwareUtilHealthReportAdapter.valueobject_to_res(
      value_object.hardware_util_health_report
    )
    logger_health_report = GetLoggerHealthReportAdapter.valueobject_to_res(
      value_object.logger_health_report
    )
    healthy = (
      config_health_report.healthy
      and database_health_report.healthy
      and hardware_util_health_report.healthy
      and logger_health_report.healthy
    )
    try:
      return GetFullHealthReportRes(
        config_health_report=config_health_report,
        database_health_report=database_health_report,
        hardware_util_health_report=hardware_util_health_report,
        logger_health_report=logger_health_report,
        healthy=healthy
      )
    except Exception as e:
      raise HealthAdapterException() from e
