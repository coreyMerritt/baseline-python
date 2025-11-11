from infrastructure.config.models.config_health_report import ConfigHealthReport
from interfaces.rest.health.dto.res.get_full_health_report_res import GetConfigHealthReportRes
from interfaces.rest.health.exceptions.health_adapter_exception import HealthAdapterException


class GetConfigHealthReportAdapter:
  @staticmethod
  def model_to_res(model: ConfigHealthReport) -> GetConfigHealthReportRes:
    try:
      return GetConfigHealthReportRes(
        healthy=model.healthy
      )
    except Exception as e:
      raise HealthAdapterException(str(e)) from e
