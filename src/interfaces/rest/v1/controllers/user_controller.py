import asyncio

from interfaces.rest.models.projectname_http_response import ProjectnameHTTPResponse
from interfaces.rest.models.projectname_request import ProjectnameRequest
from interfaces.rest.v1.dto.req.user.create_user_req import CreateUserReq
from interfaces.rest.v1.dto.req.user.update_user_req import UpdateUserReq
from interfaces.rest.v1.mappers.user.create_user_mapper import CreateUserMapper
from interfaces.rest.v1.mappers.user.delete_user_mapper import DeleteUserMapper
from interfaces.rest.v1.mappers.user.get_user_mapper import GetUserMapper
from interfaces.rest.v1.mappers.user.update_user_mapper import UpdateUserMapper
from services.user_manager import UserManager
from services.exceptions.item_creation_err import ItemCreationErr


class UserController:
  async def get_user(self, req: ProjectnameRequest, ulid: str) -> ProjectnameHTTPResponse:
    user_manager = UserManager(
      logger=req.infra.logger,
      user_repository=req.repos.user
    )
    user_som = await asyncio.to_thread(user_manager.get_user, ulid)
    get_user_res = GetUserMapper.som_to_res(user_som)
    return ProjectnameHTTPResponse(
      data=get_user_res
    )

  async def create_user(self, req: ProjectnameRequest, body: CreateUserReq) -> ProjectnameHTTPResponse:
    user_manager = UserManager(
      logger=req.infra.logger,
      user_repository=req.repos.user
    )
    create_user_service_model = CreateUserMapper.req_to_sim(body)
    create_user_som = user_manager.create_user(create_user_service_model)
    if not create_user_som:
      raise ItemCreationErr()
    create_user_res = CreateUserMapper.som_to_res(create_user_som)
    return ProjectnameHTTPResponse(
      data=create_user_res
    )

  async def update_user(self, req: ProjectnameRequest, body: UpdateUserReq) -> ProjectnameHTTPResponse:
    user_manager = UserManager(
      logger=req.infra.logger,
      user_repository=req.repos.user
    )
    update_user_service_model = UpdateUserMapper.req_to_sim(body)
    update_user_som = user_manager.update_user(update_user_service_model)
    if not update_user_som:
      raise ItemCreationErr()
    update_user_res = UpdateUserMapper.som_to_res(update_user_som)
    return ProjectnameHTTPResponse(
      data=update_user_res
    )

  async def delete_user(self, req: ProjectnameRequest, ulid: str) -> ProjectnameHTTPResponse:
    user_manager = UserManager(
      logger=req.infra.logger,
      user_repository=req.repos.user
    )
    user_som = await asyncio.to_thread(user_manager.delete_user, ulid)
    delete_user_res = DeleteUserMapper.som_to_res(user_som)
    return ProjectnameHTTPResponse(
      data=delete_user_res
    )
