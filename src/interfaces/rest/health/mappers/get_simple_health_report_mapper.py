from interfaces.rest.health.dto.res.get_simple_health_report_res import GetSimpleHealthReportRes
from shared.exceptions.mapper_err import MapperErr
from shared.models.health_reports.full_health_report import FullHealthReport


class GetSimpleHealthReportMapper:
  @staticmethod
  def model_to_res(model: FullHealthReport) -> GetSimpleHealthReportRes:
    try:
      return GetSimpleHealthReportRes(
        healthy=model.healthy
      )
    except Exception as e:
      raise MapperErr() from e
