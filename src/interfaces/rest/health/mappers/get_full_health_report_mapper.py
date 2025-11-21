from interfaces.rest.health.dto.res.get_full_health_report_res import GetFullHealthReportRes
from interfaces.rest.health.mappers.get_config_parser_health_report_mapper import GetConfigParserHealthReportMapper
from interfaces.rest.health.mappers.get_cpu_health_report_mapper import GetCpuHealthReportMapper
from interfaces.rest.health.mappers.get_database_health_report_mapper import GetDatabaseHealthReportMapper
from interfaces.rest.health.mappers.get_disk_health_report_mapper import GetDiskHealthReportMapper
from interfaces.rest.health.mappers.get_environment_health_report_mapper import GetEnvironmentHealthReportMapper
from interfaces.rest.health.mappers.get_logger_health_report_mapper import GetLoggerHealthReportMapper
from interfaces.rest.health.mappers.get_memory_health_report_mapper import GetMemoryHealthReportMapper
from interfaces.rest.health.mappers.get_typicode_health_report_mapper import GetTypicodeHealthReportMapper
from shared.exceptions.mapper_err import MapperErr
from shared.models.health_reports.full_health_report import FullHealthReport


class GetFullHealthReportMapper:
  @staticmethod
  def model_to_res(model: FullHealthReport) -> GetFullHealthReportRes:
    get_config_parser_health_report_res = GetConfigParserHealthReportMapper.model_to_res(
      model.config_parser_health_report
    )
    get_cpu_health_report_res = GetCpuHealthReportMapper.model_to_res(
      model.cpu_health_report
    )
    get_database_health_report_res = GetDatabaseHealthReportMapper.model_to_res(
      model.database_health_report
    )
    get_disk_health_report_res = GetDiskHealthReportMapper.model_to_res(
      model.disk_health_report
    )
    get_environment_health_report_res = GetEnvironmentHealthReportMapper.model_to_res(
      model.environment_health_report
    )
    get_logger_health_report_res = GetLoggerHealthReportMapper.model_to_res(
      model.logger_health_report
    )
    get_memory_health_report_res = GetMemoryHealthReportMapper.model_to_res(
      model.memory_health_report
    )
    get_typicode_health_report_res = GetTypicodeHealthReportMapper.model_to_res(
      model.typicode_health_report
    )
    try:
      return GetFullHealthReportRes(
        config_parser=get_config_parser_health_report_res,
        cpu=get_cpu_health_report_res,
        database=get_database_health_report_res,
        disk=get_disk_health_report_res,
        environment=get_environment_health_report_res,
        logger=get_logger_health_report_res,
        memory=get_memory_health_report_res,
        typicode=get_typicode_health_report_res,
        healthy=model.healthy
      )
    except Exception as e:
      raise MapperErr() from e
