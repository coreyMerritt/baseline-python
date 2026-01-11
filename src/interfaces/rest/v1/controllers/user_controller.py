import asyncio

from fastapi import HTTPException, Request

from domain.enums.user_type import UserType
from interfaces.rest.models.foo_project_name_http_response import FooProjectNameHTTPResponse
from interfaces.rest.v1.dto.req.user.create_user_req import CreateUserReq
from interfaces.rest.v1.dto.req.user.update_user_req import UpdateUserReq
from interfaces.rest.v1.mappers.user.create_user_mapper import CreateUserMapper
from interfaces.rest.v1.mappers.user.delete_user_mapper import DeleteUserMapper
from interfaces.rest.v1.mappers.user.get_user_mapper import GetUserMapper
from interfaces.rest.v1.mappers.user.update_user_mapper import UpdateUserMapper
from services.exceptions.item_creation_err import ItemCreationErr
from services.user_manager import UserManager


class UserController:
  async def get_user(self, req: Request, ulid: str) -> FooProjectNameHTTPResponse:
    self._authorize_access_by_user_ulid(req, ulid)
    user_manager = UserManager(
      user_admin_secret=req.app.state.resources.vars.users_admin_secret,
      logger=req.app.state.resources.infra.logger,
      password_hasher=req.app.state.resources.infra.password_hasher,
      user_repository=req.app.state.resources.repos.user
    )
    get_user_som = await asyncio.to_thread(user_manager.get_user, ulid)
    get_user_res = GetUserMapper.som_to_res(get_user_som)
    return FooProjectNameHTTPResponse(
      data=get_user_res
    )

  async def create_user(self, req: Request, body: CreateUserReq) -> FooProjectNameHTTPResponse:
    user_manager = UserManager(
      user_admin_secret=req.app.state.resources.vars.users_admin_secret,
      logger=req.app.state.resources.infra.logger,
      password_hasher=req.app.state.resources.infra.password_hasher,
      user_repository=req.app.state.resources.repos.user
    )
    # If trying to create a privileged user, assert admin secret is present and correct
    if body.user_type in (UserType.ADMIN.value, UserType.READ_ONLY_CLIENT.value, UserType.WRITE_CLIENT.value):
      if not body.admin_secret:
        raise HTTPException(
          status_code=403,
          detail="Not permitted to create this item",
        )
      if not body.admin_secret == req.app.state.resources.vars.users_admin_secret:
        raise HTTPException(
          status_code=401,
          detail="Invalid admin secret",
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
      user_admin_secret=req.app.state.resources.vars.users_admin_secret,
      logger=req.app.state.resources.infra.logger,
      password_hasher=req.app.state.resources.infra.password_hasher,
      user_repository=req.app.state.resources.repos.user
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
      user_admin_secret=req.app.state.resources.vars.users_admin_secret,
      logger=req.app.state.resources.infra.logger,
      password_hasher=req.app.state.resources.infra.password_hasher,
      user_repository=req.app.state.resources.repos.user
    )
    delete_user_som = await asyncio.to_thread(user_manager.delete_user, ulid)
    delete_user_res = DeleteUserMapper.som_to_res(delete_user_som)
    return FooProjectNameHTTPResponse(
      data=delete_user_res
    )

  def _authorize_access_by_user_ulid(self, req: Request, some_user_ulid: str) -> None:
    if (
      not getattr(req.state, "is_authenticated", False)
      or not getattr(req.state, "user", None)
    ):
      raise HTTPException(
        status_code=401,
        detail="Authentication required",
      )
    authenticated_user = req.state.user
    # Admins are always authorized
    if authenticated_user.user_type == UserType.ADMIN:
      return
    # Read-only clients may not handle user data
    if authenticated_user.user_type == UserType.READ_ONLY_CLIENT:
      raise HTTPException(
        status_code=403,
        detail="Not permitted to access this item",
      )
    # Write clients may not handle user data
    if authenticated_user.user_type == UserType.WRITE_CLIENT:
      raise HTTPException(
        status_code=403,
        detail="Not permitted to access this item",
      )
    # Users may handle their own data only
    if authenticated_user.user_type == UserType.STANDARD:
      if some_user_ulid != req.state.user.ulid:
        raise HTTPException(
          status_code=403,
          detail="Not permitted to access this item",
        )
      return
    # This should never trigger
    raise HTTPException(
      status_code=400,
      detail="Bad Request",
    )
