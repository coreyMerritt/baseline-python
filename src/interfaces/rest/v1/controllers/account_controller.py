import asyncio
from logging import Logger

from fastapi import HTTPException

from infrastructure.logging.log_manager import LogManager
from interfaces.rest.v1.adapters.create_account_adapter import CreateAccountAdapter
from interfaces.rest.v1.adapters.get_account_adapter import GetAccountAdapter
from interfaces.rest.v1.dto.req.create_account_req import CreateAccountReq
from interfaces.rest.v1.dto.res.create_account_res import CreateAccountRes
from interfaces.rest.v1.dto.res.get_account_res import GetAccountRes
from interfaces.rest.v1.exceptions.rest_adapter_exception import RestAdapterException
from services.account_manager import AccountManager
from services.exceptions.account_service_initialization_exception import AccountServiceInitializationException
from services.exceptions.data_exception import DataException
from services.exceptions.data_validation_exception import DataValidationException


class AccountController:
  _logger: Logger
  _account_manager: AccountManager

  def __init__(self):
    self._logger = LogManager.get_logger(self.__class__.__name__)
    self._account_manager = AccountManager()

  # NOTE: Most GETs will not use a Req, just one or more query params /account?uuid=123
  async def get_account(self, uuid: str) -> GetAccountRes:
    try:
      account = await asyncio.to_thread(self._account_manager.get_account, uuid)
      if not account:
        self._logger.warning("No existing account found for uuid: %s", uuid)
        raise HTTPException(status_code=404, detail="Account not found")
      self._logger.info("Successfully retrieved account for uuid: %s", uuid)
      return GetAccountAdapter.domain_to_res(account)
    except AccountServiceInitializationException as e:
      self._logger.error("Failed to initialize Account Service", exc_info=e)
      raise HTTPException(status_code=500, detail="Internal server error") from e
    except DataException as e:
      self._logger.error("Something went wrong at the data level", exc_info=e)
      raise HTTPException(status_code=500, detail="Internal server error") from e
    except RestAdapterException as e:
      # We drop exec_info=e for low-concern exceptions
      self._logger.warning("Bad request")
      # We give proper error codes when possible with "detail" matching the error code summary
      raise HTTPException(status_code=400, detail="Bad request") from e
    except Exception as e:
      self._logger.error("Unknown exception -- Failed to get account for uuid: %s", uuid, exc_info=e)
      raise HTTPException(status_code=500, detail="Internal server error") from e

  async def create_account(self, req: CreateAccountReq) -> CreateAccountRes:
    try:
      account = CreateAccountAdapter.req_to_domain(req)
      self._account_manager.create_account(
        uuid=account.get_uid(),
        name=account.get_name(),
        age=account.get_age(),
        account_type=account.get_account_type()
      )
      self._logger.info("Successfully created account for uuid: %s", account.get_uid())
      return CreateAccountAdapter.domain_to_res(account, "Success")
    except DataValidationException as e:
      # We drop exec_info=e for low-concern exceptions
      self._logger.warning("Bad request")
      # We give proper error codes when possible with "detail" matching the error code summary
      raise HTTPException(status_code=400, detail="Bad request") from e
    except DataException as e:
      self._logger.error("Something went wrong at the data level", exc_info=e)
      raise HTTPException(status_code=500, detail="Internal server error") from e
    except RestAdapterException as e:
      # We drop exec_info=e for low-concern exceptions
      self._logger.warning("Bad request")
      # We give proper error codes when possible with "detail" matching the error code summary
      raise HTTPException(status_code=400, detail="Bad request") from e
    except Exception as e:
      self._logger.error("Unknown exception -- Failed to create account", exc_info=e)
      raise HTTPException(status_code=500, detail="Internal server error") from e
