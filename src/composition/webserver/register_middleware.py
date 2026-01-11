from fastapi import FastAPI
from interfaces.rest.middleware.auth import AuthMiddleware
from interfaces.rest.middleware.request_id import RequestIDMiddleware
from interfaces.rest.middleware.request_logging import RequestLoggingMiddleware
from interfaces.rest.middleware.response_logging import ResponseLoggingMiddleware


def register_middleware(app: FastAPI) -> FastAPI:
  app.add_middleware(
    AuthMiddleware,
    get_authenticator=lambda: app.state.resources.infra.authenticator,
    get_logger=lambda: app.state.resources.infra.logger
  )
  app.add_middleware(
    ResponseLoggingMiddleware,
    get_logger=lambda: app.state.resources.infra.logger
  )
  app.add_middleware(
    RequestLoggingMiddleware,
    get_logger=lambda: app.state.resources.infra.logger
  )
  app.add_middleware(RequestIDMiddleware)
  return app
