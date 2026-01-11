from fastapi import FastAPI, Request

from interfaces.rest.exceptions.universal_exception_response import universal_exception_response
from services.exceptions.account_deleted_err import AccountDeletedErr
from services.exceptions.account_suspended_err import AccountSuspendedErr
from services.exceptions.bad_input_err import BadInputErr


def register_400_bad_request_handlers(app: FastAPI) -> None:
  @app.exception_handler(AccountDeletedErr)
  @app.exception_handler(AccountSuspendedErr)
  @app.exception_handler(BadInputErr)
  async def handle_400(req: Request, exc: Exception):
    MESSAGE = "Bad request"
    CODE = 400
    logger = req.app.state.resources.infra.logger
    logger.warning(
      message=MESSAGE,
      error=exc
    )
    return await universal_exception_response(MESSAGE, CODE)
