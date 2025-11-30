import time
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from infrastructure.types.logger_interface import LoggerInterface
from interfaces.rest.mappers.projectname_request_mapper import ProjectnameRequestMapper
from interfaces.rest.models.projectname_request import ProjectnameRequest


class ResponseLoggingMiddleware(BaseHTTPMiddleware):
  _get_logger: Callable[[], LoggerInterface]

  def __init__(self, app, get_logger: Callable[[], LoggerInterface]):
    self._get_logger = get_logger
    super().__init__(app)

  async def dispatch(self, request: Request, call_next):
    logger = self._get_logger()
    start = time.perf_counter()
    try:
      response: Response = await call_next(request)
    except Exception as e:
      app = request.app
      handler = app.exception_handlers.get(type(e))
      if handler:
        response = await handler(request, e)
      else:
        response = await app.exception_handlers[Exception](request, e)
    finally:
      duration_ms = (time.perf_counter() - start) * 1000.0
      req = ProjectnameRequest(request)
      raw_http_res_info = ProjectnameRequestMapper.to_raw_http_res_info(
        req=req,
        status=response.status_code,
        duration_ms=duration_ms)
      logger.http_res_info(
        message="HTTP Response",
        raw_http_res_info=raw_http_res_info
      )
    return response
