from infrastructure.environment.models.environment_health_report import EnvironmentHealthReport
from interfaces.rest.health.dto.res.get_environment_health_report_res import GetEnvironmentHealthReportRes
from shared.exceptions.mapper_err import MapperErr


class GetEnvironmentHealthReportMapper:
  @staticmethod
  def infrastructure_model_to_res(model: EnvironmentHealthReport) -> GetEnvironmentHealthReportRes:
    try:
      return GetEnvironmentHealthReportRes(
        healthy=model.healthy
      )
    except Exception as e:
      raise MapperErr() from e
