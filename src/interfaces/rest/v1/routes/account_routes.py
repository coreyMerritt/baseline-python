from fastapi import APIRouter, Depends

from interfaces.rest.models.projectname_http_response import ProjectnameHTTPResponse
from interfaces.rest.models.projectname_request import ProjectnameRequest, get_projectname_request
from interfaces.rest.v1.controllers.account_controller import AccountController
from interfaces.rest.v1.dto.req.create_account_req import CreateAccountReq

controller = AccountController()
router = APIRouter(prefix="/api/v1/account")

@router.get(
  path="",
  response_model=ProjectnameHTTPResponse,
  status_code=200
)
async def get_account(
  uuid: str,
  req: ProjectnameRequest = Depends(get_projectname_request)
) -> ProjectnameHTTPResponse:
  return await controller.get_account(
    req=req,
    uuid=uuid
  )

@router.post(
  path="",
  response_model=ProjectnameHTTPResponse,
  status_code=201
)
async def create_account(
  body: CreateAccountReq,
  req: ProjectnameRequest = Depends(get_projectname_request)
) -> ProjectnameHTTPResponse:
  return await controller.create_account(
    req=req,
    body=body
  )
