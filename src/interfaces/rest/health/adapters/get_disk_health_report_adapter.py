from interfaces.rest.exceptions.rest_adapter_err import RestAdapterErr
from interfaces.rest.health.dto.res.get_disk_health_report_res import GetDiskHealthReportRes
from shared.models.health_reports.disk_health_report import DiskHealthReport


class GetDiskHealthReportAdapter:
  @staticmethod
  def model_to_res(model: DiskHealthReport) -> GetDiskHealthReportRes:
    try:
      return GetDiskHealthReportRes(
        usage_percentage=model.usage_percentage,
        healthy=model.healthy
      )
    except Exception as e:
      raise RestAdapterErr() from e
