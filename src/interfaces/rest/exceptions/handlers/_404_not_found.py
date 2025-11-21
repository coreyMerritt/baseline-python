from fastapi import FastAPI, Request

from interfaces.rest.exceptions.projectname_httpexception import ProjectnameHTTPException
from services.exceptions.item_not_found_err import ItemNotFoundErr
from shared.types.logger_interface import LoggerInterface


def register_404_not_found_handlers(app: FastAPI, logger: LoggerInterface) -> None:
  LOGGER = logger

  @app.exception_handler(ItemNotFoundErr)
  async def handle_404(r: Request, e: Exception):
    _ = r
    LOGGER.error("Not found")
    raise ProjectnameHTTPException(
      status_code=404,
      message="Not found"
    ) from e
