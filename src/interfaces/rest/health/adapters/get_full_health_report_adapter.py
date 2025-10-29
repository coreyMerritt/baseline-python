from interfaces.rest.health.dto.res.get_full_health_report_res import GetFullHealthReportRes
from interfaces.rest.health.exceptions.health_adapter_exception import HealthAdapterException
from services.value_objects.full_health_report import FullHealthReport


class GetFullHealthReportAdapter:
  @staticmethod
  def valueobject_to_res(value_object: FullHealthReport) -> GetFullHealthReportRes:
    try:
      return GetFullHealthReportRes(
        healthy=True
      )
    except Exception as e:
      raise HealthAdapterException() from e
