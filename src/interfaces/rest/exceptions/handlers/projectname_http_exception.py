from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from interfaces.rest.exceptions.projectname_http_exception import ProjectnameHTTPException
from interfaces.rest.models.projectname_http_error import ProjectnameHTTPError
from interfaces.rest.models.projectname_http_response import ProjectnameHTTPResponse


def register_projectname_httpexception_handler(app: FastAPI) -> None:
  @app.exception_handler(ProjectnameHTTPException)
  async def projectname_httpexception_handler(r: Request, e: ProjectnameHTTPException):
    _ = r
    payload: ProjectnameHTTPResponse[Any] = ProjectnameHTTPResponse(
      data=None,
      error = ProjectnameHTTPError(
        message=e.message
      )
    )
    return JSONResponse(
      status_code=e.status_code,
      content=payload.model_dump()
    )
