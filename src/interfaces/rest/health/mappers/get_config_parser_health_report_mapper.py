from interfaces.rest.health.dto.res.get_config_parser_health_report_res import GetConfigParserHealthReportRes
from shared.exceptions.mapper_err import MapperErr
from shared.models.health_reports.config_parser_health_report import ConfigParserHealthReport


class GetConfigParserHealthReportMapper:
  @staticmethod
  def model_to_res(model: ConfigParserHealthReport) -> GetConfigParserHealthReportRes:
    try:
      return GetConfigParserHealthReportRes(
        healthy=model.healthy
      )
    except Exception as e:
      raise MapperErr() from e
