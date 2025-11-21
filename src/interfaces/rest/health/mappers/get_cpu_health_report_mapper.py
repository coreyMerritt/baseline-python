from interfaces.rest.health.dto.res.get_cpu_health_report_res import GetCpuHealthReportRes
from shared.exceptions.mapper_err import MapperErr
from shared.models.health_reports.cpu_health_report import CpuHealthReport


class GetCpuHealthReportMapper:
  @staticmethod
  def model_to_res(model: CpuHealthReport) -> GetCpuHealthReportRes:
    try:
      return GetCpuHealthReportRes(
        usage_percentage=model.usage_percentage,
        healthy=model.healthy
      )
    except Exception as e:
      raise MapperErr() from e
