from fastapi import Request

from interfaces.rest.exceptions.projectname_httpexception import ProjectnameHTTPException
from interfaces.rest.types.projectname_fastapi import ProjectnameFastAPI
from interfaces.rest.types.projectname_request import ProjectnameRequest
from services.exceptions.item_creation_err import ItemCreationErr
from services.exceptions.service_initialization_err import ServiceInitializationErr
from services.exceptions.service_unavailable_err import ServiceUnavailableErr


def register_500_internal_server_error_handlers(app: ProjectnameFastAPI) -> None:
  @app.exception_handler(Exception)
  @app.exception_handler(ItemCreationErr)
  @app.exception_handler(ServiceInitializationErr)
  @app.exception_handler(ServiceUnavailableErr)
  async def handle_500(req: Request, exc: Exception):
    projectname_request = ProjectnameRequest(req)
    logger = projectname_request.infra.logger
    logger.error("Caught Unhandled Exception", exc_info=exc)
    raise ProjectnameHTTPException(
      status_code=500,
      message="Internal server error"
    ) from exc
