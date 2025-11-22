from fastapi import FastAPI

from interfaces.rest.exceptions.handlers._400_bad_request import register_400_bad_request_handlers
from interfaces.rest.exceptions.handlers._404_not_found import register_404_not_found_handlers
from interfaces.rest.exceptions.handlers._500_internal_server_error import register_500_internal_server_error_handlers


def register_exception_handlers(app: FastAPI) -> FastAPI:
  register_400_bad_request_handlers(app)
  register_404_not_found_handlers(app)
  register_500_internal_server_error_handlers(app)
  return app
