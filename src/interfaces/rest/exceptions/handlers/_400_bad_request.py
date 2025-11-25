from fastapi import Request

from interfaces.rest.exceptions.handlers._universal_handler_response import universal_handler_response
from interfaces.rest.models.projectname_fastapi import ProjectnameFastAPI
from interfaces.rest.models.projectname_request import ProjectnameRequest
from services.exceptions.bad_input_err import BadInputErr


def register_400_bad_request_handlers(app: ProjectnameFastAPI) -> None:
  @app.exception_handler(BadInputErr)
  async def handle_400(request: Request, exception: Exception):
    MESSAGE = "Bad request"
    CODE = 400
    req = ProjectnameRequest(request)
    logger = req.infra.logger
    logger.warning(
      message=MESSAGE,
      error=exception
    )
    return universal_handler_response(MESSAGE, CODE)
