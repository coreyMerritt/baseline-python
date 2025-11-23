import asyncio

from interfaces.rest.models.projectname_http_response import ProjectnameHTTPResponse
from interfaces.rest.types.projectname_request import ProjectnameRequest
from interfaces.rest.v1.dto.req.create_account_req import CreateAccountReq
from interfaces.rest.v1.mappers.create_account_mapper import CreateAccountMapper
from interfaces.rest.v1.mappers.get_account_mapper import GetAccountMapper
from services.account_manager import AccountManager
from services.exceptions.item_creation_err import ItemCreationErr


class AccountController:
  async def get_account(self, req: ProjectnameRequest, uuid: str) -> ProjectnameHTTPResponse:
    account_manager = AccountManager(
      req.infra.logger,
      req.repos.account
    )
    account_som = await asyncio.to_thread(account_manager.get_account, uuid)
    get_account_res = GetAccountMapper.som_to_res(account_som)
    return ProjectnameHTTPResponse(
      data=get_account_res
    )

  async def create_account(self, req: ProjectnameRequest, body: CreateAccountReq) -> ProjectnameHTTPResponse:
    account_manager = AccountManager(
      req.infra.logger,
      req.repos.account
    )
    create_account_service_model = CreateAccountMapper.req_to_servicemodel(body)
    create_account_som = account_manager.create_account(create_account_service_model)
    if not create_account_som:
      raise ItemCreationErr()
    create_account_res = CreateAccountMapper.servicemodel_to_res(create_account_som, "Success")
    return ProjectnameHTTPResponse(
      data=create_account_res
    )
