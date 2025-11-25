from fastapi import Request

from interfaces.rest.exceptions.handlers._universal_handler_response import universal_handler_response
from interfaces.rest.models.projectname_fastapi import ProjectnameFastAPI
from interfaces.rest.models.projectname_request import ProjectnameRequest
from services.exceptions.item_not_found_err import ItemNotFoundErr


def register_404_not_found_handlers(app: ProjectnameFastAPI) -> None:
  @app.exception_handler(ItemNotFoundErr)
  async def handle_404(request: Request, exception: Exception):
    MESSAGE = "Not found"
    CODE = 404
    req = ProjectnameRequest(request)
    logger = req.infra.logger
    logger.error(
      message=MESSAGE,
      error=exception
    )
    return universal_handler_response(MESSAGE, CODE)
