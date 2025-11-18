from interfaces.rest.exceptions.rest_adapter_err import RestAdapterErr
from interfaces.rest.health.dto.res.get_config_parser_health_report_res import GetConfigParserHealthReportRes
from shared.models.health_reports.config_parser_health_report import ConfigParserHealthReport


class GetConfigParserHealthReportAdapter:
  @staticmethod
  def model_to_res(model: ConfigParserHealthReport) -> GetConfigParserHealthReportRes:
    try:
      return GetConfigParserHealthReportRes(
        healthy=model.healthy
      )
    except Exception as e:
      raise RestAdapterErr() from e
