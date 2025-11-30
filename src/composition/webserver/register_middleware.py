from interfaces.rest.middleware.request_id import RequestIDMiddleware
from interfaces.rest.middleware.request_logging import RequestLoggingMiddleware
from interfaces.rest.middleware.response_logging import ResponseLoggingMiddleware
from interfaces.rest.models.projectname_fastapi import ProjectnameFastAPI


def register_middleware(app: ProjectnameFastAPI) -> ProjectnameFastAPI:
  app.add_middleware(ResponseLoggingMiddleware, get_logger=lambda: app.infra.logger)
  app.add_middleware(RequestLoggingMiddleware, get_logger=lambda: app.infra.logger)
  app.add_middleware(RequestIDMiddleware)
  return app
