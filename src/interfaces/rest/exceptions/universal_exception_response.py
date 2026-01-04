from typing import Any

from fastapi.responses import JSONResponse

from interfaces.rest.models.foo_project_name_http_error import FooProjectNameHTTPError
from interfaces.rest.models.foo_project_name_http_response import FooProjectNameHTTPResponse


async def universal_exception_response(
  message: str,
  code: int
) -> JSONResponse:
  response_model = FooProjectNameHTTPResponse[Any](
    data=None,
    error=FooProjectNameHTTPError(message=message)
  )
  return JSONResponse(
    status_code=code,
    content=response_model.model_dump(),
  )
