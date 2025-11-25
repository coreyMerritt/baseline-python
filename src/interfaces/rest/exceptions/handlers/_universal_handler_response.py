from typing import Any

from fastapi.responses import JSONResponse

from interfaces.rest.models.projectname_http_error import ProjectnameHTTPError
from interfaces.rest.models.projectname_http_response import ProjectnameHTTPResponse


async def universal_handler_response(
  message: str,
  code: int
) -> JSONResponse:
  response_model = ProjectnameHTTPResponse[Any](
    data=None,
    error=ProjectnameHTTPError(message=message)
  )
  return JSONResponse(
    status_code=code,
    content=response_model.model_dump(),
  )
