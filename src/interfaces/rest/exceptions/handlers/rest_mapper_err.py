from fastapi import FastAPI, Request

from interfaces.rest.exceptions.projectname_http_exception import ProjectnameHTTPException
from shared.exceptions.mapper_err import MapperErr
from shared.types.logger_interface import LoggerInterface


def register_rest_mapper_exception_handler(app: FastAPI, logger: LoggerInterface) -> None:
  LOGGER = logger

  @app.exception_handler(MapperErr)
  async def handle_rest_mapper_exception(r: Request, e: Exception):
    _ = r
    LOGGER.warning("Bad request")
    raise ProjectnameHTTPException(
      status_code=400,
      message="Bad Request"
    ) from e
