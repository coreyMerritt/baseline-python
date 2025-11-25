from fastapi import Request

from interfaces.rest.exceptions.projectname_httpexception import ProjectnameHTTPException
from interfaces.rest.models.projectname_fastapi import ProjectnameFastAPI
from interfaces.rest.models.projectname_request import ProjectnameRequest
from services.exceptions.item_not_found_err import ItemNotFoundErr


def register_404_not_found_handlers(app: ProjectnameFastAPI) -> None:
  @app.exception_handler(ItemNotFoundErr)
  async def handle_404(r: Request, e: Exception):
    req = ProjectnameRequest(r)
    logger = req.infra.logger
    logger.error(
      message="Not found",
      error=e
    )
    raise ProjectnameHTTPException(
      status_code=404,
      message="Not found"
    ) from e
