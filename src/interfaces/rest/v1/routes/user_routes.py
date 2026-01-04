from fastapi import APIRouter, Depends

from interfaces.rest.models.foo_project_name_http_response import FooProjectNameHTTPResponse
from interfaces.rest.models.foo_project_name_request import FooProjectNameRequest, get_foo_project_name_request
from interfaces.rest.v1.controllers.user_controller import UserController
from interfaces.rest.v1.dto.req.user.create_user_req import CreateUserReq
from interfaces.rest.v1.dto.req.user.update_user_req import UpdateUserReq

controller = UserController()
router = APIRouter(prefix="/api/v1/user")

@router.get(
  path="",
  response_model=FooProjectNameHTTPResponse,
  status_code=200
)
async def get_user(
  ulid: str,
  req: FooProjectNameRequest = Depends(get_foo_project_name_request)
) -> FooProjectNameHTTPResponse:
  return await controller.get_user(
    req=req,
    ulid=ulid
  )

@router.post(
  path="",
  response_model=FooProjectNameHTTPResponse,
  status_code=201
)
async def create_user(
  body: CreateUserReq,
  req: FooProjectNameRequest = Depends(get_foo_project_name_request)
) -> FooProjectNameHTTPResponse:
  return await controller.create_user(
    req=req,
    body=body
  )

@router.put(
  path="",
  response_model=FooProjectNameHTTPResponse,
  status_code=200
)
async def update_user(
  body: UpdateUserReq,
  req: FooProjectNameRequest = Depends(get_foo_project_name_request)
) -> FooProjectNameHTTPResponse:
  return  await controller.update_user(
    req=req,
    body=body
  )

@router.delete(
  path="",
  response_model=FooProjectNameHTTPResponse,
  status_code=200
)
async def delete_user(
  ulid: str,
  req: FooProjectNameRequest = Depends(get_foo_project_name_request)
) -> FooProjectNameHTTPResponse:
  return await controller.delete_user(
    req=req,
    ulid=ulid
  )
