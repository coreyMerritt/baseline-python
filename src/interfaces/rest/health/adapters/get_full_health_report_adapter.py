from interfaces.rest.exceptions.rest_adapter_err import RestAdapterErr
from interfaces.rest.health.adapters.get_config_parser_health_report_adapter import GetConfigParserHealthReportAdapter
from interfaces.rest.health.adapters.get_cpu_health_report_adapter import GetCpuHealthReportAdapter
from interfaces.rest.health.adapters.get_database_health_report_adapter import GetDatabaseHealthReportAdapter
from interfaces.rest.health.adapters.get_disk_health_report_adapter import GetDiskHealthReportAdapter
from interfaces.rest.health.adapters.get_environment_health_report_adapter import GetEnvironmentHealthReportAdapter
from interfaces.rest.health.adapters.get_logger_health_report_adapter import GetLoggerHealthReportAdapter
from interfaces.rest.health.adapters.get_memory_health_report_adapter import GetMemoryHealthReportAdapter
from interfaces.rest.health.adapters.get_typicode_health_report_adapter import GetTypicodeHealthReportAdapter
from interfaces.rest.health.dto.res.get_full_health_report_res import GetFullHealthReportRes
from shared.models.health_reports.full_health_report import FullHealthReport


class GetFullHealthReportAdapter:
  @staticmethod
  def model_to_res(model: FullHealthReport) -> GetFullHealthReportRes:
    config_parser_health_report = GetConfigParserHealthReportAdapter.model_to_res(
      model.config_parser_health_report
    )
    cpu_health_report = GetCpuHealthReportAdapter.model_to_res(
      model.cpu_health_report
    )
    database_health_report = GetDatabaseHealthReportAdapter.model_to_res(
      model.database_health_report
    )
    disk_health_report = GetDiskHealthReportAdapter.model_to_res(
      model.disk_health_report
    )
    environment_health_report = GetEnvironmentHealthReportAdapter.model_to_res(
      model.environment_health_report
    )
    logger_health_report = GetLoggerHealthReportAdapter.model_to_res(
      model.logger_health_report
    )
    memory_health_report = GetMemoryHealthReportAdapter.model_to_res(
      model.memory_health_report
    )
    typicode_health_report = GetTypicodeHealthReportAdapter.model_to_res(
      model.typicode_health_report
    )
    healthy = (
      config_parser_health_report.healthy
      and cpu_health_report.healthy
      and database_health_report.healthy
      and disk_health_report.healthy
      and environment_health_report.healthy
      and logger_health_report.healthy
      and memory_health_report.healthy
      and typicode_health_report.healthy
    )
    try:
      return GetFullHealthReportRes(
        config_parser_health_report=config_parser_health_report,
        cpu_health_report=cpu_health_report,
        database_health_report=database_health_report,
        disk_health_report=disk_health_report,
        environment_health_report=environment_health_report,
        logger_health_report=logger_health_report,
        memory_health_report=memory_health_report,
        typicode_health_report=typicode_health_report,
        healthy=healthy
      )
    except Exception as e:
      raise RestAdapterErr() from e
