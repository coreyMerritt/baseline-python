from fastapi import Request

from interfaces.rest.exceptions.universal_exception_response import universal_exception_response
from interfaces.rest.models.foo_project_name_fastapi import FooProjectNameFastAPI
from interfaces.rest.models.foo_project_name_request import FooProjectNameRequest
from services.exceptions.item_not_found_err import ItemNotFoundErr


def register_404_not_found_handlers(app: FooProjectNameFastAPI) -> None:
  @app.exception_handler(ItemNotFoundErr)
  async def handle_404(request: Request, exception: Exception):
    MESSAGE = "Not found"
    CODE = 404
    req = FooProjectNameRequest(request)
    logger = req.infra.logger
    logger.error(
      message=MESSAGE,
      error=exception
    )
    return await universal_exception_response(MESSAGE, CODE)
