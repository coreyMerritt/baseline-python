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
  async def handle_500(r: Request, e: Exception):
    if "ProjectnameHTTPException" in str(type(e)):
      raise e
    req = ProjectnameRequest(r)
    logger = req.infra.logger
    logger.err(
      message="Caught Unhandled Exception",
      error=e,
      correlation_id=req.correlation_id,
      endpoint=req.endpoint,
      request_id=req.request_id
    )
    raise ProjectnameHTTPException(
      status_code=500,
      message="Internal server error"
    ) from e
