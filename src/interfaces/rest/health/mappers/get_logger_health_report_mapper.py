from interfaces.rest.health.dto.res.get_full_health_report_res import GetLoggerHealthReportRes
from shared.exceptions.mapper_err import MapperErr
from shared.models.health_reports.logger_health_report import LoggerHealthReport


class GetLoggerHealthReportMapper:
  @staticmethod
  def model_to_res(model: LoggerHealthReport) -> GetLoggerHealthReportRes:
    try:
      return GetLoggerHealthReportRes(
        healthy=model.healthy
      )
    except Exception as e:
      raise MapperErr() from e
