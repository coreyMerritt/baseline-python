from fastapi import APIRouter, HTTPException

from infrastructure.logging.log_manager import LogManager
from interfaces.rest.health.controllers.health_controller import HealthController
from interfaces.rest.health.dto.res.get_full_health_report_res import GetFullHealthReportRes

router = APIRouter(prefix="/api/health")
controller = HealthController()
logger = LogManager.get_logger("AccountRoutes")

# NOTE: Most GETs will not use a Req, just one or more query params ex) /account?uuid=123
@router.get("/", response_model=GetFullHealthReportRes)
async def get_full_health_report() -> GetFullHealthReportRes:
  try:
    return await controller.get_full_health_report()
  except HTTPException:
    raise
  except Exception as e:
    logger.critical("Unexpected non-HTTPException in routes", exc_info=e)
    raise HTTPException(status_code=500, detail="Internal server error") from e
