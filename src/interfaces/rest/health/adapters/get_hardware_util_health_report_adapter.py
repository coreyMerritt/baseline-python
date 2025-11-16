from interfaces.rest.exceptions.rest_adapter_err import RestAdapterErr
from interfaces.rest.health.dto.res.get_full_health_report_res import GetHardwareUtilHealthReportRes
from shared.models.health_reports.hardware_util_health_report import HardwareUtilHealthReport


class GetHardwareUtilHealthReportAdapter:
  @staticmethod
  def model_to_res(model: HardwareUtilHealthReport) -> GetHardwareUtilHealthReportRes:
    try:
      return GetHardwareUtilHealthReportRes(
        healthy=model.healthy
      )
    except Exception as e:
      raise RestAdapterErr(str(e)) from e
