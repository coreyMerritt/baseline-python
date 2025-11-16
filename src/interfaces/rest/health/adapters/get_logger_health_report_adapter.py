from interfaces.rest.exceptions.rest_adapter_err import RestAdapterErr
from interfaces.rest.health.dto.res.get_full_health_report_res import GetLoggerHealthReportRes
from shared.models.health_reports.logger_health_report import LoggerHealthReport


class GetLoggerHealthReportAdapter:
  @staticmethod
  def model_to_res(model: LoggerHealthReport) -> GetLoggerHealthReportRes:
    try:
      return GetLoggerHealthReportRes(
        healthy=model.healthy
      )
    except Exception as e:
      raise RestAdapterErr(str(e)) from e
