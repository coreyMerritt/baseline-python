from typing import Any

from fastapi.responses import JSONResponse

from interfaces.rest.exceptions.projectname_httpexception import ProjectnameHTTPException
from interfaces.rest.models.projectname_http_error import ProjectnameHTTPError
from interfaces.rest.models.projectname_http_response import ProjectnameHTTPResponse
from interfaces.rest.types.projectname_fastapi import ProjectnameFastAPI
from interfaces.rest.types.projectname_request import ProjectnameRequest


def register_projectname_httpexception_handler(app: ProjectnameFastAPI) -> None:
  @app.exception_handler(ProjectnameHTTPException)
  async def projectname_httpexception_handler(r: ProjectnameRequest, e: ProjectnameHTTPException):
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
