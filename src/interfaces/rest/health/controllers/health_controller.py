import asyncio

from interfaces.rest.health.mappers.get_full_health_report_mapper import GetFullHealthReportMapper
from interfaces.rest.health.mappers.get_simple_health_report_mapper import GetSimpleHealthReportMapper
from interfaces.rest.models.foo_project_name_http_response import FooProjectNameHTTPResponse
from interfaces.rest.models.foo_project_name_request import FooProjectNameRequest
from services.health_manager import HealthManager
from services.models.outputs.full_health_report_som import FullHealthReportSOM


class HealthController:
  async def get_simple_health_report(self, req: FooProjectNameRequest) -> FooProjectNameHTTPResponse:
    health_report_som = await self._get_health_report_som(req)
    get_simple_health_report_res = GetSimpleHealthReportMapper.som_to_res(health_report_som)
    return FooProjectNameHTTPResponse(
      data=get_simple_health_report_res
    )

  async def get_full_health_report(self, req: FooProjectNameRequest) -> FooProjectNameHTTPResponse:
    health_report_som = await self._get_health_report_som(req)
    get_full_health_report_res = GetFullHealthReportMapper.som_to_res(health_report_som)
    return FooProjectNameHTTPResponse(
      data=get_full_health_report_res
    )

  async def _get_health_report_som(self, req: FooProjectNameRequest) -> FullHealthReportSOM:
    health_manager = HealthManager(
      logger=req.infra.logger,
      config_parser=req.infra.config_parser,
      cpu=req.infra.cpu,
      database=req.infra.database,
      disk=req.infra.disk,
      environment=req.infra.environment,
      memory=req.infra.memory,
      typicode_client=req.infra.typicode_client
    )
    return await asyncio.to_thread(
      health_manager.get_full_health_report
    )
