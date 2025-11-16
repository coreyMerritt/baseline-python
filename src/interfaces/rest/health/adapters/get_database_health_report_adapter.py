from interfaces.rest.exceptions.rest_adapter_err import RestAdapterErr
from interfaces.rest.health.dto.res.get_full_health_report_res import GetDatabaseHealthReportRes
from shared.models.health_reports.database_health_report import DatabaseHealthReport


class GetDatabaseHealthReportAdapter:
  @staticmethod
  def model_to_res(model: DatabaseHealthReport) -> GetDatabaseHealthReportRes:
    try:
      return GetDatabaseHealthReportRes(
        healthy=model.healthy
      )
    except Exception as e:
      raise RestAdapterErr(str(e)) from e
