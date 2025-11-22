from infrastructure.config.models.config_parser_health_report import ConfigParserHealthReport
from interfaces.rest.health.dto.res.get_config_parser_health_report_res import GetConfigParserHealthReportRes
from shared.exceptions.mapper_err import MapperErr


class GetConfigParserHealthReportMapper:
  @staticmethod
  def infrastructure_model_to_res(model: ConfigParserHealthReport) -> GetConfigParserHealthReportRes:
    try:
      return GetConfigParserHealthReportRes(
        healthy=model.healthy
      )
    except Exception as e:
      raise MapperErr() from e
