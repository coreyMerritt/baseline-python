from composition.infrastructure_instances import logger
from interfaces.rest.middleware.request_id import RequestIDMiddleware
from interfaces.rest.middleware.request_logging import RequestLoggingMiddleware
from interfaces.rest.middleware.response_logging import ResponseLoggingMiddleware
from interfaces.rest.models.projectname_fastapi import ProjectnameFastAPI


def register_middleware(app: ProjectnameFastAPI) -> ProjectnameFastAPI:
  app.add_middleware(ResponseLoggingMiddleware, logger=logger)
  app.add_middleware(RequestLoggingMiddleware, logger=logger)
  app.add_middleware(RequestIDMiddleware)
  return app
