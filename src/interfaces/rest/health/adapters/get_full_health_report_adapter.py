from interfaces.rest.exceptions.rest_adapter_err import RestAdapterErr
from interfaces.rest.health.adapters.get_config_health_report_adapter import GetConfigHealthReportAdapter
from interfaces.rest.health.adapters.get_database_health_report_adapter import GetDatabaseHealthReportAdapter
from interfaces.rest.health.adapters.get_hardware_util_health_report_adapter import GetHardwareUtilHealthReportAdapter
from interfaces.rest.health.adapters.get_logger_health_report_adapter import GetLoggerHealthReportAdapter
from interfaces.rest.health.dto.res.get_full_health_report_res import GetFullHealthReportRes
from shared.models.health_reports.full_health_report import FullHealthReport


class GetFullHealthReportAdapter:
  @staticmethod
  def model_to_res(model: FullHealthReport) -> GetFullHealthReportRes:
    config_health_report = GetConfigHealthReportAdapter.model_to_res(
      model.config_health_report
    )
    database_health_report = GetDatabaseHealthReportAdapter.model_to_res(
      model.database_health_report
    )
    hardware_util_health_report = GetHardwareUtilHealthReportAdapter.model_to_res(
      model.hardware_util_health_report
    )
    logger_health_report = GetLoggerHealthReportAdapter.model_to_res(
      model.logger_health_report
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
      raise RestAdapterErr() from e
