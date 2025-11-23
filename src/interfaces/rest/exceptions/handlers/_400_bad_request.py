from fastapi import Request

from interfaces.rest.exceptions.projectname_httpexception import ProjectnameHTTPException
from interfaces.rest.types.projectname_fastapi import ProjectnameFastAPI
from interfaces.rest.types.projectname_request import ProjectnameRequest
from services.exceptions.bad_input_err import BadInputErr


def register_400_bad_request_handlers(app: ProjectnameFastAPI) -> None:
  @app.exception_handler(BadInputErr)
  async def handle_400(req: Request, exc: Exception):
    projectname_request = ProjectnameRequest(req)
    logger = projectname_request.infra.logger
    logger.warning("Bad request")
    raise ProjectnameHTTPException(
      status_code=400,
      message="Bad ProjectnameRequest"
    ) from exc
