from fastapi import FastAPI, Request

from interfaces.rest.exceptions.projectname_httpexception import ProjectnameHTTPException
from services.exceptions.bad_input_err import BadInputErr


def register_400_bad_request_handlers(app: FastAPI) -> None:
  @app.exception_handler(BadInputErr)
  async def handle_400(r: Request, e: Exception):
    logger = r.state.infra.logger
    logger.warning("Bad request")
    raise ProjectnameHTTPException(
      status_code=400,
      message="Bad Request"
    ) from e
