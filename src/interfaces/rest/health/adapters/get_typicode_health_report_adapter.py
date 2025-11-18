from interfaces.rest.exceptions.rest_adapter_err import RestAdapterErr
from interfaces.rest.health.dto.res.get_typicode_health_report_res import GetTypicodeHealthReportRes
from shared.models.health_reports.typicode_health_report import TypicodeHealthReport


class GetTypicodeHealthReportAdapter:
  @staticmethod
  def model_to_res(model: TypicodeHealthReport) -> GetTypicodeHealthReportRes:
    try:
      return GetTypicodeHealthReportRes(
        healthy=model.healthy
      )
    except Exception as e:
      raise RestAdapterErr() from e
