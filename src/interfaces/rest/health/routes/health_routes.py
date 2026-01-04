from fastapi import APIRouter, Depends

from interfaces.rest.health.controllers.health_controller import HealthController
from interfaces.rest.models.foo_project_name_http_response import FooProjectNameHTTPResponse
from interfaces.rest.models.foo_project_name_request import FooProjectNameRequest, get_foo_project_name_request

controller = HealthController()
router = APIRouter(prefix="/api/health")

@router.get("", response_model=FooProjectNameHTTPResponse)
async def get_simple_health_report(
  req: FooProjectNameRequest = Depends(get_foo_project_name_request)
) -> FooProjectNameHTTPResponse:
  return await controller.get_simple_health_report(
    req=req
  )

@router.get("/full", response_model=FooProjectNameHTTPResponse)
async def get_full_health_report(
  req: FooProjectNameRequest = Depends(get_foo_project_name_request)
) -> FooProjectNameHTTPResponse:
  return await controller.get_full_health_report(
    req=req
  )
