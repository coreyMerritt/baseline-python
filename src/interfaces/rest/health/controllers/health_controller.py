import asyncio

from fastapi import Request

from interfaces.rest.health.mappers.get_full_health_report_mapper import GetFullHealthReportMapper
from interfaces.rest.health.mappers.get_simple_health_report_mapper import GetSimpleHealthReportMapper
from interfaces.rest.models.projectname_http_response import ProjectnameHTTPResponse
from services.health_manager import HealthManager
from shared.models.configs.cpu_config import CpuConfig
from shared.models.configs.disk_config import DiskConfig
from shared.models.configs.external_services_config import ExternalServicesConfig
from shared.models.configs.memory_config import MemoryConfig
from shared.models.configs.typicode_config import TypicodeConfig
from shared.models.health_reports.full_health_report import FullHealthReport
from shared.types.logger_interface import LoggerInterface


class HealthController:
  _req: Request
  _logger: LoggerInterface
  _cpu_config: CpuConfig
  _disk_config: DiskConfig
  _external_services_config: ExternalServicesConfig
  _memory_config: MemoryConfig
  _typicode_config: TypicodeConfig
  _health_manager: HealthManager

  def __init__(self, req: Request):
    self._req = req
    self._logger = req.app.state.logger
    self._database = req.app.state.database
    self._cpu_config = req.app.state.config.cpu
    self._disk_config = req.app.state.config.disk
    self._external_services_config = req.app.state.config.external_services
    self._memory_config = req.app.state.config.memory
    self._typicode_config = req.app.state.config.typicode
    self._health_manager = HealthManager(
      req.app.state.logger
    )

  async def get_simple_health_report(self) -> ProjectnameHTTPResponse:
    health_report = await self._get_health_report()
    get_simple_health_report_res = GetSimpleHealthReportMapper.model_to_res(health_report)
    return ProjectnameHTTPResponse(
      data=get_simple_health_report_res
    )

  async def get_full_health_report(self) -> ProjectnameHTTPResponse:
    health_report = await self._get_health_report()
    get_full_health_report_res = GetFullHealthReportMapper.model_to_res(health_report)
    return ProjectnameHTTPResponse(
      data=get_full_health_report_res
    )

  async def _get_health_report(self) -> FullHealthReport:
    return await asyncio.to_thread(
      self._health_manager.get_full_health_report,
      self._database,
      self._cpu_config,
      self._disk_config,
      self._external_services_config,
      self._memory_config,
      self._typicode_config
    )
