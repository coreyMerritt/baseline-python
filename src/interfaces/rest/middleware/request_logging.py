from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from infrastructure.types.logger_interface import LoggerInterface
from interfaces.rest.mappers.projectname_request_mapper import ProjectnameRequestMapper
from interfaces.rest.models.projectname_request import ProjectnameRequest


class RequestLoggingMiddleware(BaseHTTPMiddleware):
  def __init__(self, app, logger: LoggerInterface):
    super().__init__(app)
    self._logger = logger

  async def dispatch(self, request: Request, call_next):
    req = ProjectnameRequest(request)
    raw_http_req_log = ProjectnameRequestMapper.to_raw_http_req_info(req)
    self._logger.http_req_info(
      message="HTTP Request",
      raw_http_req_info=raw_http_req_log
    )
    return await call_next(request)
