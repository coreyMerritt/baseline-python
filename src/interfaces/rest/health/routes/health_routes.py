from fastapi import APIRouter

from infrastructure.logging.log_manager import LogManager
from interfaces.rest.health.controllers.health_controller import HealthController
from interfaces.rest.health.dto.res.get_full_health_report_res import GetFullHealthReportRes

router = APIRouter(prefix="/api/health")

# NOTE: Most GETs will not use a Req, just one or more query params ex) /account?uuid=123
@router.get("/", response_model=GetFullHealthReportRes)
async def get_full_health_report() -> GetFullHealthReportRes:
  controller = HealthController()
  return await controller.get_full_health_report()
