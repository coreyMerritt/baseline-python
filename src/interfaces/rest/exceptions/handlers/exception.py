from logging import Logger

from fastapi import FastAPI, Request

from interfaces.rest.exceptions.projectname_http_exception import ProjectnameHTTPException


def register_unhandled_exception_handler(app: FastAPI, logger: Logger) -> None:
  LOGGER = logger

  @app.exception_handler(Exception)
  async def handle_unhandled_exception(r: Request, e: Exception):
    _ = r
    LOGGER.error("Caught Unhandled Exception", exc_info=e)
    raise ProjectnameHTTPException(
      status_code=500,
      message="Internal server error"
    ) from e
