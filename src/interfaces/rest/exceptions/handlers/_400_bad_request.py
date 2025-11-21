from fastapi import FastAPI, Request

from interfaces.rest.exceptions.projectname_httpexception import ProjectnameHTTPException
from services.exceptions.bad_input_err import BadInputErr
from shared.exceptions.mapper_err import MapperErr
from shared.types.logger_interface import LoggerInterface


def register_400_bad_request_handlers(app: FastAPI, logger: LoggerInterface) -> None:
  LOGGER = logger


  @app.exception_handler(BadInputErr)
  @app.exception_handler(MapperErr)
  async def handle_400(r: Request, e: Exception):
    _ = r
    LOGGER.warning("Bad request")
    raise ProjectnameHTTPException(
      status_code=400,
      message="Bad Request"
    ) from e
