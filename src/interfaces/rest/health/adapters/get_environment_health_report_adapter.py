from interfaces.rest.exceptions.rest_adapter_err import RestAdapterErr
from interfaces.rest.health.dto.res.get_environment_health_report_res import GetEnvironmentHealthReportRes
from shared.models.health_reports.environment_health_report import EnvironmentHealthReport


class GetEnvironmentHealthReportAdapter:
  @staticmethod
  def model_to_res(model: EnvironmentHealthReport) -> GetEnvironmentHealthReportRes:
    try:
      return GetEnvironmentHealthReportRes(
        healthy=model.healthy
      )
    except Exception as e:
      raise RestAdapterErr() from e
