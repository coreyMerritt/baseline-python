from interfaces.rest.health.dto.res.get_full_health_report_res import GetLoggerHealthReportRes
from interfaces.rest.exceptions.health_adapter_exception import HealthAdapterException
from shared.models.health_reports.logger_health_report import LoggerHealthReport


class GetLoggerHealthReportAdapter:
  @staticmethod
  def model_to_res(model: LoggerHealthReport) -> GetLoggerHealthReportRes:
    try:
      return GetLoggerHealthReportRes(
        healthy=model.healthy
      )
    except Exception as e:
      raise HealthAdapterException(str(e)) from e
