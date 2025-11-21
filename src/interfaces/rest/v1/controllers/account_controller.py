import asyncio

from fastapi import Request

from interfaces.rest.models.projectname_http_response import ProjectnameHTTPResponse
from interfaces.rest.v1.dto.req.create_account_req import CreateAccountReq
from interfaces.rest.v1.mappers.create_account_mapper import CreateAccountMapper
from interfaces.rest.v1.mappers.get_account_mapper import GetAccountMapper
from services.account_manager import AccountManager
from services.exceptions.item_creation_err import ItemCreationErr
from shared.types.logger_interface import LoggerInterface


class AccountController:
  _req: Request
  _logger: LoggerInterface
  _account_manager: AccountManager

  def __init__(self, req: Request):
    self._req = req
    self._logger = req.app.state.logger
    self._account_manager = AccountManager(
      req.app.state.logger,
      req.app.state.repository.account
    )

  async def get_account(self, uuid: str) -> ProjectnameHTTPResponse:
    account_som = await asyncio.to_thread(self._account_manager.get_account, uuid)
    get_account_res = GetAccountMapper.som_to_res(account_som)
    return ProjectnameHTTPResponse(
      data=get_account_res
    )

  async def create_account(self, req: CreateAccountReq) -> ProjectnameHTTPResponse:
    create_account_service_model = CreateAccountMapper.req_to_servicemodel(req)
    create_account_som = self._account_manager.create_account(create_account_service_model)
    if not create_account_som:
      raise ItemCreationErr()
    create_account_res = CreateAccountMapper.servicemodel_to_res(create_account_som, "Success")
    return ProjectnameHTTPResponse(
      data=create_account_res
    )
