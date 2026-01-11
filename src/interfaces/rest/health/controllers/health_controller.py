import asyncio

from fastapi import HTTPException, Request

from domain.enums.user_type import UserType
from interfaces.rest.health.mappers.get_full_health_report_mapper import GetFullHealthReportMapper
from interfaces.rest.health.mappers.get_simple_health_report_mapper import GetSimpleHealthReportMapper
from interfaces.rest.models.foo_project_name_http_response import FooProjectNameHTTPResponse
from services.health_manager import HealthManager
from services.models.outputs.full_health_report_som import FullHealthReportSOM


class HealthController:
  async def get_simple_health_report(self, req: Request) -> FooProjectNameHTTPResponse:
    health_report_som = await self._get_health_report_som(req)
    get_simple_health_report_res = GetSimpleHealthReportMapper.som_to_res(health_report_som)
    return FooProjectNameHTTPResponse(
      data=get_simple_health_report_res
    )

  async def get_full_health_report(self, req: Request) -> FooProjectNameHTTPResponse:
    self._authorize_full_health_report_access(req)
    health_report_som = await self._get_health_report_som(req)
    get_full_health_report_res = GetFullHealthReportMapper.som_to_res(health_report_som)
    return FooProjectNameHTTPResponse(
      data=get_full_health_report_res
    )

  async def _get_health_report_som(self, req: Request) -> FullHealthReportSOM:
    health_manager = HealthManager(
      logger=req.app.state.resources.infra.logger,
      config_parser=req.app.state.resources.infra.config_parser,
      cpu=req.app.state.resources.infra.cpu,
      database=req.app.state.resources.infra.database,
      disk=req.app.state.resources.infra.disk,
      environment=req.app.state.resources.infra.environment,
      memory=req.app.state.resources.infra.memory
    )
    return await asyncio.to_thread(
      health_manager.get_full_health_report
    )

  def _authorize_full_health_report_access(self, req: Request) -> None:
    if (
      not getattr(req.state, "is_authenticated", False)
      or not getattr(req.state, "user", None)
    ):
      raise HTTPException(
        status_code=401,
        detail="Authentication required",
      )
    authenticated_user = req.state.user
    # Admins are always authorized
    if authenticated_user.user_type == UserType.ADMIN:
      return
    # Read-only clients may see full health reports
    if authenticated_user.user_type == UserType.READ_ONLY_CLIENT:
      return
    # Write clients may see full health reports
    if authenticated_user.user_type == UserType.WRITE_CLIENT:
      return
    # Standard users may not see full health reports
    if authenticated_user.user_type == UserType.STANDARD:
      raise HTTPException(
        status_code=403,
        detail="Not permitted to access this item",
      )
    # This should never trigger
    raise HTTPException(
      status_code=400,
      detail="Bad Request",
    )
