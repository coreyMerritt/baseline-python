from fastapi import Request

from interfaces.rest.exceptions.projectname_httpexception import ProjectnameHTTPException
from interfaces.rest.types.projectname_fastapi import ProjectnameFastAPI
from interfaces.rest.types.projectname_request import ProjectnameRequest
from services.exceptions.item_not_found_err import ItemNotFoundErr


def register_404_not_found_handlers(app: ProjectnameFastAPI) -> None:
  @app.exception_handler(ItemNotFoundErr)
  async def handle_404(req: Request, exc: Exception):
    projectname_request = ProjectnameRequest(req)
    logger = projectname_request.infra.logger
    logger.error("Not found")
    raise ProjectnameHTTPException(
      status_code=404,
      message="Not found"
    ) from exc
