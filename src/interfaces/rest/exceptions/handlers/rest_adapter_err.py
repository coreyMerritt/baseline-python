from logging import Logger

from fastapi import FastAPI, Request

from interfaces.rest.exceptions.projectname_http_exception import ProjectnameHTTPException
from interfaces.rest.exceptions.rest_adapter_err import RestAdapterErr


def register_rest_adapter_exception_handler(app: FastAPI, logger: Logger) -> None:
  LOGGER = logger

  @app.exception_handler(RestAdapterErr)
  async def handle_rest_adapter_exception(r: Request, e: Exception):
    _ = r
    LOGGER.warning("Bad request")
    raise ProjectnameHTTPException(
      status_code=400,
      message="Bad Request"
    ) from e
