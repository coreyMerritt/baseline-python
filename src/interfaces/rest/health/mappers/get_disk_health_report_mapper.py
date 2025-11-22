from infrastructure.disk.models.disk_health_report import DiskHealthReport
from interfaces.rest.health.dto.res.get_disk_health_report_res import GetDiskHealthReportRes
from shared.exceptions.mapper_err import MapperErr


class GetDiskHealthReportMapper:
  @staticmethod
  def infrastructure_model_to_res(model: DiskHealthReport) -> GetDiskHealthReportRes:
    try:
      return GetDiskHealthReportRes(
        usage_percentage=model.usage_percentage,
        healthy=model.healthy
      )
    except Exception as e:
      raise MapperErr() from e
