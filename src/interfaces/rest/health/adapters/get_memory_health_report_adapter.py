from interfaces.rest.exceptions.rest_adapter_err import RestAdapterErr
from interfaces.rest.health.dto.res.get_memory_health_report_res import GetMemoryHealthReportRes
from shared.models.health_reports.memory_health_report import MemoryHealthReport


class GetMemoryHealthReportAdapter:
  @staticmethod
  def model_to_res(model: MemoryHealthReport) -> GetMemoryHealthReportRes:
    try:
      return GetMemoryHealthReportRes(
        usage_percentage=model.usage_percentage,
        healthy=model.healthy
      )
    except Exception as e:
      raise RestAdapterErr() from e
