from fastapi import APIRouter, Request

from interfaces.rest.health.controllers.health_controller import HealthController
from interfaces.rest.models.foo_project_name_http_response import FooProjectNameHTTPResponse

controller = HealthController()
router = APIRouter(prefix="/api/health")

@router.get("", response_model=FooProjectNameHTTPResponse)
async def get_simple_health_report(req: Request) -> FooProjectNameHTTPResponse:
  return await controller.get_simple_health_report(
    req=req
  )

@router.get("/full", response_model=FooProjectNameHTTPResponse)
async def get_full_health_report(req: Request) -> FooProjectNameHTTPResponse:
  return await controller.get_full_health_report(
    req=req
  )
