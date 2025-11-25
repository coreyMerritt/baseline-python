from fastapi import APIRouter, Depends

from interfaces.rest.health.controllers.health_controller import HealthController
from interfaces.rest.models.projectname_http_response import ProjectnameHTTPResponse
from interfaces.rest.models.projectname_request import ProjectnameRequest, get_projectname_request

controller = HealthController()
router = APIRouter(prefix="/api/health")

@router.get("", response_model=ProjectnameHTTPResponse)
async def get_simple_health_report(
  req: ProjectnameRequest = Depends(get_projectname_request)
) -> ProjectnameHTTPResponse:
  return await controller.get_simple_health_report(
    req=req
  )

@router.get("/full", response_model=ProjectnameHTTPResponse)
async def get_full_health_report(
  req: ProjectnameRequest = Depends(get_projectname_request)
) -> ProjectnameHTTPResponse:
  return await controller.get_full_health_report(
    req=req
  )
