from interfaces.rest.exceptions.rest_adapter_err import RestAdapterErr
from interfaces.rest.health.dto.res.get_cpu_health_report_res import GetCpuHealthReportRes
from shared.models.health_reports.cpu_health_report import CpuHealthReport


class GetCpuHealthReportAdapter:
  @staticmethod
  def model_to_res(model: CpuHealthReport) -> GetCpuHealthReportRes:
    try:
      return GetCpuHealthReportRes(
        healthy=model.healthy
      )
    except Exception as e:
      raise RestAdapterErr() from e
