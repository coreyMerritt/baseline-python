from interfaces.rest.exceptions.rest_adapter_err import RestAdapterErr
from interfaces.rest.health.dto.res.get_full_health_report_res import GetConfigHealthReportRes
from shared.models.health_reports.config_health_report import ConfigHealthReport


class GetConfigHealthReportAdapter:
  @staticmethod
  def model_to_res(model: ConfigHealthReport) -> GetConfigHealthReportRes:
    try:
      return GetConfigHealthReportRes(
        healthy=model.healthy
      )
    except Exception as e:
      raise RestAdapterErr(str(e)) from e
