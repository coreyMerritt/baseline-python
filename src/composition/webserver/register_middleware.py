from interfaces.rest.middleware.request_id import RequestIDMiddleware
from interfaces.rest.middleware.request_logging import RequestLoggingMiddleware
from interfaces.rest.middleware.response_logging import ResponseLoggingMiddleware
from interfaces.rest.models.foo_project_name_fastapi import FooProjectNameFastAPI


def register_middleware(app: FooProjectNameFastAPI) -> FooProjectNameFastAPI:
  app.add_middleware(ResponseLoggingMiddleware, get_logger=lambda: app.resources.infra.logger)
  app.add_middleware(RequestLoggingMiddleware, get_logger=lambda: app.resources.infra.logger)
  app.add_middleware(RequestIDMiddleware)
  return app
