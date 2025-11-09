from interfaces.rest.health.dto.res.get_full_health_report_res import GetDatabaseHealthReportRes
from interfaces.rest.health.exceptions.health_adapter_exception import HealthAdapterException
from services.value_objects.full_health_report import DatabaseHealthReport


class GetDatabaseHealthReportAdapter:
  @staticmethod
  def valueobject_to_res(value_object: DatabaseHealthReport) -> GetDatabaseHealthReportRes:
    try:
      return GetDatabaseHealthReportRes(
        healthy=value_object.healthy
      )
    except Exception as e:
      raise HealthAdapterException() from e
