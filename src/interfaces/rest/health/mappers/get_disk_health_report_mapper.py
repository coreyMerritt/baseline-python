from interfaces.rest.health.dto.res.get_disk_health_report_res import GetDiskHealthReportRes
from shared.exceptions.mapper_err import MapperErr
from shared.models.health_reports.disk_health_report import DiskHealthReport


class GetDiskHealthReportMapper:
  @staticmethod
  def model_to_res(model: DiskHealthReport) -> GetDiskHealthReportRes:
    try:
      return GetDiskHealthReportRes(
        usage_percentage=model.usage_percentage,
        healthy=model.healthy
      )
    except Exception as e:
      raise MapperErr() from e
