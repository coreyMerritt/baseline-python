from interfaces.rest.health.dto.res.abc_get_health_report_res import GetHealthReportRes


class GetLoggerHealthReportRes(GetHealthReportRes):
  healthy: bool
