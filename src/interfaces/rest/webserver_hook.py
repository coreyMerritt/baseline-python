from types import SimpleNamespace

from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager

from interfaces.rest.exceptions.app_initialization_err import AppInitializationErr
from interfaces.rest.exceptions.handlers.exception import register_unhandled_exception_handler
from interfaces.rest.exceptions.handlers.projectname_http_exception import register_projectname_httpexception_handler
from interfaces.rest.exceptions.handlers.rest_adapter_err import register_rest_adapter_exception_handler
from interfaces.rest.health.routes import health_routes
from interfaces.rest.v1.routes import account_routes, blog_routes
from shared.shared_infrastructure import (DATABASE_CONFIG, EXTERNAL_SERVICES_CONFIG, HEALTH_CHECK_CONFIG, LOGGER_CONFIG,
                                          database, logger)


def create_app() -> FastAPI:
  @asynccontextmanager
  async def lifespan(app: FastAPI):
    # --- Startup ---
    try:
      config = SimpleNamespace()
      config.database = DATABASE_CONFIG
      config.external_services = EXTERNAL_SERVICES_CONFIG
      config.health_check = HEALTH_CHECK_CONFIG
      config.logger = LOGGER_CONFIG
      app.state.config = config
      app.state.database = database
      app.state.logger = logger
    except Exception as e:
      raise AppInitializationErr() from e

    yield  # Application runs during this period

    # --- Shutdown ---
    app.state.database.dispose()

  app = FastAPI(lifespan=lifespan)
  app = __register_exception_handlers(app)
  app = __register_routes(app)
  return app

def __register_exception_handlers(app: FastAPI) -> FastAPI:
  register_rest_adapter_exception_handler(app, logger)
  register_unhandled_exception_handler(app, logger)
  register_projectname_httpexception_handler(app)
  return app

def __register_routes(app: FastAPI) -> FastAPI:
  app.include_router(account_routes.router)
  app.include_router(blog_routes.router)
  app.include_router(health_routes.router)
  return app


if __name__ == "__main__":
  create_app()
