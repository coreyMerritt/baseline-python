import asyncio
from logging import Logger

from fastapi import Request

from interfaces.rest.exceptions.projectname_http_exception import ProjectnameHTTPException
from interfaces.rest.exceptions.rest_adapter_exception import RestAdapterException
from interfaces.rest.models.projectname_http_response import ProjectnameHTTPResponse
from interfaces.rest.v1.adapters.create_account_adapter import CreateAccountAdapter
from interfaces.rest.v1.adapters.get_account_adapter import GetAccountAdapter
from interfaces.rest.v1.dto.req.create_account_req import CreateAccountReq
from services.account_manager import AccountManager
from services.exceptions.data_exception import DataException
from services.exceptions.data_validation_exception import DataValidationException
from services.log_manager import LogManager


class AccountController:
  _req: Request
  _logger: Logger
  _account_manager: AccountManager

  def __init__(self, req: Request):
    self._req = req
    self._logger = LogManager.get_logger(self.__class__.__name__)
    self._account_manager = AccountManager(req.app.state.db)

  async def get_account(self, uuid: str) -> ProjectnameHTTPResponse:
    try:
      account = await asyncio.to_thread(self._account_manager.get_account, uuid)
      if not account:
        self._logger.warning("No existing account found for uuid: %s", uuid)
        raise ProjectnameHTTPException(
          status_code=404,
          message="Account not found"
        )
      self._logger.info("Successfully retrieved account for uuid: %s", uuid)
      get_account_res = GetAccountAdapter.domain_to_res(account)
      return ProjectnameHTTPResponse(
        data=get_account_res
      )
    except DataException as e:
      self._logger.error("Something went wrong at the data level", exc_info=e)
      raise ProjectnameHTTPException(
        status_code=500,
        message="Internal server error"
      ) from e
    except RestAdapterException as e:
      # We drop exec_info=e for low-concern exceptions
      self._logger.warning("Bad request")
      raise ProjectnameHTTPException(
        status_code=400,
        message="Bad request"
      ) from e

  async def create_account(self, req: CreateAccountReq) -> ProjectnameHTTPResponse:
    try:
      account = CreateAccountAdapter.req_to_domain(req)
      self._account_manager.create_account(
        uuid=account.get_uuid(),
        name=account.get_name(),
        age=account.get_age(),
        account_type=account.get_account_type()
      )
      self._logger.info("Successfully created account for uuid: %s", account.get_uuid())
      create_account_res = CreateAccountAdapter.domain_to_res(account, "Success")
      return ProjectnameHTTPResponse(
        data=create_account_res
      )
    except DataValidationException as e:
      # We drop exec_info=e for low-concern exceptions
      self._logger.warning("Bad request")
      raise ProjectnameHTTPException(
        status_code=400,
        message="Bad request"
      ) from e
    except DataException as e:
      self._logger.error("Something went wrong at the data level", exc_info=e)
      raise ProjectnameHTTPException(
        status_code=500,
        message="Internal server error"
      ) from e
    except RestAdapterException as e:
      # We drop exec_info=e for low-concern exceptions
      self._logger.warning("Bad request")
      raise ProjectnameHTTPException(
        status_code=400,
        message="Bad request"
      ) from e
