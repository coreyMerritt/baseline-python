import asyncio

from fastapi import Request

from interfaces.rest.health.mappers.get_full_health_report_mapper import GetFullHealthReportMapper
from interfaces.rest.health.mappers.get_simple_health_report_mapper import GetSimpleHealthReportMapper
from interfaces.rest.models.projectname_http_response import ProjectnameHTTPResponse
from services.health_manager import HealthManager
from services.models.outputs.full_health_report_som import FullHealthReportSOM


class HealthController:
  async def get_simple_health_report(self, req: Request) -> ProjectnameHTTPResponse:
    health_report_som = await self._get_health_report_som(req)
    get_simple_health_report_res = GetSimpleHealthReportMapper.som_to_res(health_report_som)
    return ProjectnameHTTPResponse(
      data=get_simple_health_report_res
    )

  async def get_full_health_report(self, req: Request) -> ProjectnameHTTPResponse:
    health_report_som = await self._get_health_report_som(req)
    get_full_health_report_res = GetFullHealthReportMapper.som_to_res(health_report_som)
    return ProjectnameHTTPResponse(
      data=get_full_health_report_res
    )

  async def _get_health_report_som(self, req: Request) -> FullHealthReportSOM:
    health_manager = HealthManager(
      logger=req.app.state.infra.logger,
      config_parser=req.app.state.infra.config_parser,
      cpu=req.app.state.infra.cpu,
      database=req.app.state.infra.database,
      disk=req.app.state.infra.disk,
      environment=req.app.state.infra.environment,
      memory=req.app.state.infra.memory,
      typicode_client=req.app.state.infra.typicode_client
    )
    return await asyncio.to_thread(
      health_manager.get_full_health_report
    )
