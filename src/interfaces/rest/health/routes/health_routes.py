from fastapi import APIRouter, Request

from interfaces.rest.health.controllers.health_controller import HealthController
from interfaces.rest.models.projectname_http_response import ProjectnameHTTPResponse

router = APIRouter(prefix="/api/health")

# NOTE: Most GETs will not use a Req, just one or more query params ex) /account?uuid=123
@router.get("", response_model=ProjectnameHTTPResponse)
async def get_full_health_report(request: Request) -> ProjectnameHTTPResponse:
  controller = HealthController(request)
  return await controller.get_full_health_report()
