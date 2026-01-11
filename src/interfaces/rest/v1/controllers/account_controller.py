import asyncio

from fastapi import Request

from interfaces.rest.models.foo_project_name_http_response import FooProjectNameHTTPResponse
from interfaces.rest.v1.dto.req.account.create_account_req import CreateAccountReq
from interfaces.rest.v1.dto.req.account.update_account_req import UpdateAccountReq
from interfaces.rest.v1.mappers.account.create_account_mapper import CreateAccountMapper
from interfaces.rest.v1.mappers.account.delete_account_mapper import DeleteAccountMapper
from interfaces.rest.v1.mappers.account.get_account_mapper import GetAccountMapper
from interfaces.rest.v1.mappers.account.update_account_mapper import UpdateAccountMapper
from services.account_manager import AccountManager
from services.exceptions.item_creation_err import ItemCreationErr


class AccountController:
  async def get_account(self, req: Request, ulid: str) -> FooProjectNameHTTPResponse:
    account_manager = AccountManager(
      logger=req.app.state.resources.infra.logger,
      account_repository=req.app.state.resources.repos.account,
      role_repository=req.app.state.resources.repos.role
    )
    account_som = await asyncio.to_thread(account_manager.get_account, ulid)
    get_account_res = GetAccountMapper.som_to_res(account_som)
    return FooProjectNameHTTPResponse(
      data=get_account_res
    )

  async def create_account(self, req: Request, body: CreateAccountReq) -> FooProjectNameHTTPResponse:
    account_manager = AccountManager(
      logger=req.app.state.resources.infra.logger,
      account_repository=req.app.state.resources.repos.account,
      role_repository=req.app.state.resources.repos.role
    )
    create_account_service_model = CreateAccountMapper.req_to_sim(body)
    create_account_som = account_manager.create_account(create_account_service_model)
    if not create_account_som:
      raise ItemCreationErr()
    create_account_res = CreateAccountMapper.som_to_res(create_account_som)
    return FooProjectNameHTTPResponse(
      data=create_account_res
    )

  async def update_account(self, req: Request, body: UpdateAccountReq) -> FooProjectNameHTTPResponse:
    account_manager = AccountManager(
      logger=req.app.state.resources.infra.logger,
      account_repository=req.app.state.resources.repos.account,
      role_repository=req.app.state.resources.repos.role
    )
    update_account_service_model = UpdateAccountMapper.req_to_sim(body)
    update_account_som = account_manager.update_account(update_account_service_model)
    if not update_account_som:
      raise ItemCreationErr()
    update_account_res = UpdateAccountMapper.som_to_res(update_account_som)
    return FooProjectNameHTTPResponse(
      data=update_account_res
    )

  async def delete_account(self, req: Request, ulid: str) -> FooProjectNameHTTPResponse:
    account_manager = AccountManager(
      logger=req.app.state.resources.infra.logger,
      account_repository=req.app.state.resources.repos.account,
      role_repository=req.app.state.resources.repos.role
    )
    account_som = await asyncio.to_thread(account_manager.delete_account, ulid)
    delete_account_res = DeleteAccountMapper.som_to_res(account_som)
    return FooProjectNameHTTPResponse(
      data=delete_account_res
    )
