import asyncio

from fastapi import Request

from interfaces.rest.health.mappers.get_full_health_report_mapper import GetFullHealthReportMapper
from interfaces.rest.health.mappers.get_simple_health_report_mapper import GetSimpleHealthReportMapper
from interfaces.rest.models.projectname_http_response import ProjectnameHTTPResponse
from services.health_manager import HealthManager
from shared.models.health_reports.full_health_report import FullHealthReport


class HealthController:
  async def get_simple_health_report(self, req: Request) -> ProjectnameHTTPResponse:
    health_report = await self._get_health_report(req)
    get_simple_health_report_res = GetSimpleHealthReportMapper.model_to_res(health_report)
    return ProjectnameHTTPResponse(
      data=get_simple_health_report_res
    )

  async def get_full_health_report(self, req: Request) -> ProjectnameHTTPResponse:
    health_report = await self._get_health_report(req)
    get_full_health_report_res = GetFullHealthReportMapper.model_to_res(health_report)
    return ProjectnameHTTPResponse(
      data=get_full_health_report_res
    )

  async def _get_health_report(self, req: Request) -> FullHealthReport:
    health_manager = HealthManager(
      req.app.state.logger
    )
    return await asyncio.to_thread(
      health_manager.get_full_health_report,
      req.app.state.database,
      req.app.state.config.cpu,
      req.app.state.config.disk,
      req.app.state.config.external_services,
      req.app.state.config.memory,
      req.app.state.config.typicode
    )
