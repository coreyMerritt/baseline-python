from fastapi import Request

from interfaces.rest.exceptions.universal_exception_response import universal_exception_response
from interfaces.rest.models.foo_project_name_fastapi import FooProjectNameFastAPI
from interfaces.rest.models.foo_project_name_request import FooProjectNameRequest
from services.exceptions.account_deleted_err import AccountDeletedErr
from services.exceptions.account_suspended_err import AccountSuspendedErr
from services.exceptions.bad_input_err import BadInputErr


def register_400_bad_request_handlers(app: FooProjectNameFastAPI) -> None:
  @app.exception_handler(AccountDeletedErr)
  @app.exception_handler(AccountSuspendedErr)
  @app.exception_handler(BadInputErr)
  async def handle_400(request: Request, exception: Exception):
    MESSAGE = "Bad request"
    CODE = 400
    req = FooProjectNameRequest(request)
    logger = req.infra.logger
    logger.warning(
      message=MESSAGE,
      error=exception
    )
    return await universal_exception_response(MESSAGE, CODE)
