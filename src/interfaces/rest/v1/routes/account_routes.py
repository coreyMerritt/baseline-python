from fastapi import APIRouter, Request

from interfaces.rest.models.foo_project_name_http_response import FooProjectNameHTTPResponse
from interfaces.rest.v1.controllers.account_controller import AccountController
from interfaces.rest.v1.dto.req.account.create_account_req import CreateAccountReq
from interfaces.rest.v1.dto.req.account.update_account_req import UpdateAccountReq

controller = AccountController()
router = APIRouter(prefix="/api/v1/account")

@router.get(
  path="",
  response_model=FooProjectNameHTTPResponse,
  status_code=200
)
async def get_account(
  ulid: str,
  req: Request
) -> FooProjectNameHTTPResponse:
  return await controller.get_account(
    req=req,
    ulid=ulid
  )

@router.post(
  path="",
  response_model=FooProjectNameHTTPResponse,
  status_code=201
)
async def create_account(
  body: CreateAccountReq,
  req: Request
) -> FooProjectNameHTTPResponse:
  return await controller.create_account(
    req=req,
    body=body
  )

@router.put(
  path="",
  response_model=FooProjectNameHTTPResponse,
  status_code=200
)
async def update_account(
  body: UpdateAccountReq,
  req: Request
) -> FooProjectNameHTTPResponse:
  return  await controller.update_account(
    req=req,
    body=body
  )

@router.delete(
  path="",
  response_model=FooProjectNameHTTPResponse,
  status_code=200
)
async def delete_account(
  ulid: str,
  req: Request
) -> FooProjectNameHTTPResponse:
  return await controller.delete_account(
    req=req,
    ulid=ulid
  )
