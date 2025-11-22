from infrastructure.external_services.models.typicode_health_report import TypicodeHealthReport
from interfaces.rest.health.dto.res.get_typicode_health_report_res import GetTypicodeHealthReportRes


class GetTypicodeHealthReportMapper:
  @staticmethod
  def infrastructure_model_to_res(model: TypicodeHealthReport) -> GetTypicodeHealthReportRes:
    return GetTypicodeHealthReportRes(
      healthy=model.healthy
    )
