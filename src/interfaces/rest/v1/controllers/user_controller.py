import asyncio

from fastapi import HTTPException, Request

from interfaces.rest.models.foo_project_name_http_response import FooProjectNameHTTPResponse
from interfaces.rest.v1.dto.req.user.create_user_req import CreateUserReq
from interfaces.rest.v1.dto.req.user.update_user_req import UpdateUserReq
from interfaces.rest.v1.mappers.user.create_user_mapper import CreateUserMapper
from interfaces.rest.v1.mappers.user.delete_user_mapper import DeleteUserMapper
from interfaces.rest.v1.mappers.user.get_user_mapper import GetUserMapper
from interfaces.rest.v1.mappers.user.update_user_mapper import UpdateUserMapper
from services.user_manager import UserManager
from services.exceptions.item_creation_err import ItemCreationErr


class UserController:
  async def get_user(self, req: Request, ulid: str) -> FooProjectNameHTTPResponse:
    self._authorize_access_by_user_ulid(req, ulid)
    user_manager = UserManager(
      logger=req.app.state.resources.infra.logger,
      password_hasher=req.app.state.resources.infra.password_hasher,
      user_repository=req.app.state.resources.repos.user,
      user_credential_repository=req.app.state.resources.repos.user_credential
    )
    get_user_som = await asyncio.to_thread(user_manager.get_user, ulid)
    get_user_res = GetUserMapper.som_to_res(get_user_som)
    return FooProjectNameHTTPResponse(
      data=get_user_res
    )

  async def create_user(self, req: Request, body: CreateUserReq) -> FooProjectNameHTTPResponse:
    user_manager = UserManager(
      logger=req.app.state.resources.infra.logger,
      password_hasher=req.app.state.resources.infra.password_hasher,
      user_repository=req.app.state.resources.repos.user,
      user_credential_repository=req.app.state.resources.repos.user_credential
    )
    create_user_service_model = CreateUserMapper.req_to_sim(body)
    create_user_som = await asyncio.to_thread(user_manager.create_user, create_user_service_model)
    if not create_user_som:
      raise ItemCreationErr()
    create_user_res = CreateUserMapper.som_to_res(create_user_som)
    return FooProjectNameHTTPResponse(
      data=create_user_res
    )

  async def update_user(self, req: Request, body: UpdateUserReq) -> FooProjectNameHTTPResponse:
    self._authorize_access_by_user_ulid(req, body.ulid)
    user_manager = UserManager(
      logger=req.app.state.resources.infra.logger,
      password_hasher=req.app.state.resources.infra.password_hasher,
      user_repository=req.app.state.resources.repos.user,
      user_credential_repository=req.app.state.resources.repos.user_credential
    )
    update_user_service_model = UpdateUserMapper.req_to_sim(body)
    update_user_som = await asyncio.to_thread(user_manager.update_user, update_user_service_model)
    if not update_user_som:
      raise ItemCreationErr()
    update_user_res = UpdateUserMapper.som_to_res(update_user_som)
    return FooProjectNameHTTPResponse(
      data=update_user_res
    )

  async def delete_user(self, req: Request, ulid: str) -> FooProjectNameHTTPResponse:
    self._authorize_access_by_user_ulid(req, ulid)
    user_manager = UserManager(
      logger=req.app.state.resources.infra.logger,
      password_hasher=req.app.state.resources.infra.password_hasher,
      user_repository=req.app.state.resources.repos.user,
      user_credential_repository=req.app.state.resources.repos.user_credential
    )
    delete_user_som = await asyncio.to_thread(user_manager.delete_user, ulid)
    delete_user_res = DeleteUserMapper.som_to_res(delete_user_som)
    return FooProjectNameHTTPResponse(
      data=delete_user_res
    )

  def _authorize_access_by_user_ulid(self, req: Request, some_user_ulid: str) -> None:
    if (
      not getattr(req.state, "is_authenticated", False)
      or not getattr(req.state, "user_ulid", None)
    ):
      raise HTTPException(
        status_code=401,
        detail="Authentication required",
      )
    if some_user_ulid != req.state.user_ulid:
      raise HTTPException(
        status_code=403,
        detail="Not permitted to access this item",
      )
