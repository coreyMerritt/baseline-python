from fastapi import FastAPI, Request

from interfaces.rest.exceptions.projectname_httpexception import ProjectnameHTTPException
from services.exceptions.item_creation_err import ItemCreationErr
from services.exceptions.service_initialization_err import ServiceInitializationErr
from services.exceptions.service_unavailable_err import ServiceUnavailableErr


def register_500_internal_server_error_handlers(app: FastAPI) -> None:
  @app.exception_handler(Exception)
  @app.exception_handler(ItemCreationErr)
  @app.exception_handler(ServiceInitializationErr)
  @app.exception_handler(ServiceUnavailableErr)
  async def handle_500(r: Request, e: Exception):
    logger = r.state.infra.logger
    logger.error("Caught Unhandled Exception", exc_info=e)
    raise ProjectnameHTTPException(
      status_code=500,
      message="Internal server error"
    ) from e
