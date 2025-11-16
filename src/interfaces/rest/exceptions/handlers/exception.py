from fastapi import FastAPI, Request

from interfaces.rest.exceptions.projectname_http_exception import ProjectnameHTTPException
from services.log_manager import LogManager


def register_unhandled_exception_handler(app: FastAPI) -> None:
  @app.exception_handler(Exception)
  async def handle_unhandled_exception(r: Request, e: Exception):
    _ = r
    logger = LogManager.get_logger("Unhandled Exception Handler")
    logger.error("Caught Unhandled Exception", exc_info=e)
    raise ProjectnameHTTPException(
      status_code=500,
      message="Internal server error"
    ) from e
