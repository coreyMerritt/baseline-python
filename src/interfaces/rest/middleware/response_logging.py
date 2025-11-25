import time

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from infrastructure.types.logger_interface import LoggerInterface
from interfaces.rest.mappers.projectname_request_mapper import ProjectnameRequestMapper
from interfaces.rest.models.projectname_request import ProjectnameRequest


class ResponseLoggingMiddleware(BaseHTTPMiddleware):
  def __init__(self, app, logger: LoggerInterface):
    super().__init__(app)
    self._logger = logger

  async def dispatch(self, request: Request, call_next):
    start = time.perf_counter()
    response: Response = await call_next(request)
    duration_ms = (time.perf_counter() - start) * 1000.0
    req = ProjectnameRequest(request)
    raw_http_res_info = ProjectnameRequestMapper.to_raw_http_res_info(
      req=req,
      status=response.status_code,
      duration_ms=duration_ms)
    self._logger.http_res_info(
      message="HTTP Response",
      raw_http_res_info=raw_http_res_info
    )
    return response
