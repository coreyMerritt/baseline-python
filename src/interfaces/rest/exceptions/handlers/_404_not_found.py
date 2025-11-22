from fastapi import FastAPI, Request

from interfaces.rest.exceptions.projectname_httpexception import ProjectnameHTTPException
from services.exceptions.item_not_found_err import ItemNotFoundErr


def register_404_not_found_handlers(app: FastAPI) -> None:
  @app.exception_handler(ItemNotFoundErr)
  async def handle_404(r: Request, e: Exception):
    logger = r.state.infra.logger
    logger.error("Not found")
    raise ProjectnameHTTPException(
      status_code=404,
      message="Not found"
    ) from e
