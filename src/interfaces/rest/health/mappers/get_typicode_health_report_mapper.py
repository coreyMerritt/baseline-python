from infrastructure.external_services.models.typicode_health_report import TypicodeHealthReport
from interfaces.rest.health.dto.res.get_typicode_health_report_res import GetTypicodeHealthReportRes
from shared.exceptions.mapper_err import MapperErr


class GetTypicodeHealthReportMapper:
  @staticmethod
  def infrastructure_model_to_res(model: TypicodeHealthReport) -> GetTypicodeHealthReportRes:
    try:
      return GetTypicodeHealthReportRes(
        healthy=model.healthy
      )
    except Exception as e:
      raise MapperErr() from e
