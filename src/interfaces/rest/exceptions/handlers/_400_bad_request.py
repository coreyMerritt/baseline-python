from fastapi import Request

from interfaces.rest.exceptions.projectname_httpexception import ProjectnameHTTPException
from interfaces.rest.types.projectname_fastapi import ProjectnameFastAPI
from interfaces.rest.types.projectname_request import ProjectnameRequest
from services.exceptions.bad_input_err import BadInputErr


def register_400_bad_request_handlers(app: ProjectnameFastAPI) -> None:
  @app.exception_handler(BadInputErr)
  async def handle_400(r: Request, e: Exception):
    req = ProjectnameRequest(r)
    logger = req.infra.logger
    logger.warning(
      message="Bad request",
      error=e,
      correlation_id=req.correlation_id,
      endpoint=req.endpoint,
      request_id=req.request_id
    )
    raise ProjectnameHTTPException(
      status_code=400,
      message="Bad Request"
    ) from e
