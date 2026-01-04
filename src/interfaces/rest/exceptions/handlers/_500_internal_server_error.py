from fastapi import Request

from interfaces.rest.exceptions.universal_exception_response import universal_exception_response
from interfaces.rest.models.foo_project_name_fastapi import FooProjectNameFastAPI
from interfaces.rest.models.foo_project_name_request import FooProjectNameRequest
from services.exceptions.item_creation_err import ItemCreationErr
from services.exceptions.service_initialization_err import ServiceInitializationErr
from services.exceptions.service_unavailable_err import ServiceUnavailableErr


def register_500_internal_server_error_handlers(app: FooProjectNameFastAPI) -> None:
  @app.exception_handler(Exception)
  @app.exception_handler(ItemCreationErr)
  @app.exception_handler(ServiceInitializationErr)
  @app.exception_handler(ServiceUnavailableErr)
  async def handle_500(request: Request, exception: Exception):
    MESSAGE = "Internal server error"
    CODE = 500
    req = FooProjectNameRequest(request)
    logger = req.infra.logger
    logger.error(
      message=f"[Caught Unhandled Exception] {MESSAGE}",
      error=exception
    )
    return await universal_exception_response(MESSAGE, CODE)
