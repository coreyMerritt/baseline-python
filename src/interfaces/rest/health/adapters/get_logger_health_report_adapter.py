from interfaces.rest.health.dto.res.get_full_health_report_res import GetLoggerHealthReportRes
from interfaces.rest.health.exceptions.health_adapter_exception import HealthAdapterException
from services.value_objects.full_health_report import LoggerHealthReport


class GetLoggerHealthReportAdapter:
  @staticmethod
  def valueobject_to_res(value_object: LoggerHealthReport) -> GetLoggerHealthReportRes:
    try:
      return GetLoggerHealthReportRes(
        healthy=value_object.healthy
      )
    except Exception as e:
      raise HealthAdapterException() from e
