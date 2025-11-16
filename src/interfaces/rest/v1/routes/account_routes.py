from fastapi import APIRouter, Request

from interfaces.rest.models.projectname_http_response import ProjectnameHTTPResponse
from interfaces.rest.v1.controllers.account_controller import AccountController
from interfaces.rest.v1.dto.req.create_account_req import CreateAccountReq

router = APIRouter(prefix="/api/v1/account")

@router.get(
  path="",
  response_model=ProjectnameHTTPResponse,
  status_code=200
)
async def get_account(req: Request, uuid: str) -> ProjectnameHTTPResponse:
  controller = AccountController(req)
  return await controller.get_account(uuid)

@router.post(
  path="",
  response_model=ProjectnameHTTPResponse,
  status_code=201
)
async def create_account(req: Request, create_account_req: CreateAccountReq) -> ProjectnameHTTPResponse:
  controller = AccountController(req)
  return await controller.create_account(create_account_req)
