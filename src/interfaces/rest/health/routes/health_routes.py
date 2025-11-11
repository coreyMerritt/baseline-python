from fastapi import APIRouter, Request

from interfaces.rest.health.controllers.health_controller import HealthController
from interfaces.rest.health.dto.res.get_full_health_report_res import GetFullHealthReportRes

router = APIRouter(prefix="/api/health")

# NOTE: Most GETs will not use a Req, just one or more query params ex) /account?uuid=123
@router.get("", response_model=GetFullHealthReportRes)
async def get_full_health_report(request: Request) -> GetFullHealthReportRes:
  controller = HealthController(request)
  return await controller.get_full_health_report()
