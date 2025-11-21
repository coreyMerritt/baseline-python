from types import SimpleNamespace

from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager

from interfaces.rest.exceptions.handlers._400_bad_request import register_400_bad_request_handlers
from interfaces.rest.exceptions.handlers._404_not_found import register_404_not_found_handlers
from interfaces.rest.exceptions.handlers._500_internal_server_error import register_500_internal_server_error_handlers
from interfaces.rest.health.routes import health_routes
from interfaces.rest.v1.routes import account_routes, blog_routes
from shared.shared_infrastructure import (CPU_CONFIG, DATABASE_CONFIG, DISK_CONFIG, EXTERNAL_SERVICES_CONFIG,
                                          LOGGER_CONFIG, MEMORY_CONFIG, TYPICODE_CONFIG, account_repository,
                                          blog_post_repository, logger)


def create_app() -> FastAPI:
  @asynccontextmanager
  async def lifespan(app: FastAPI):
    # --- Startup ---
    config = SimpleNamespace()
    config.cpu = CPU_CONFIG
    config.database = DATABASE_CONFIG
    config.disk = DISK_CONFIG
    config.external_services = EXTERNAL_SERVICES_CONFIG
    config.memory = MEMORY_CONFIG
    config.typicode = TYPICODE_CONFIG
    config.logger = LOGGER_CONFIG
    repository = SimpleNamespace()
    repository.account = account_repository
    repository.blog_post = blog_post_repository
    app.state.config = config
    app.state.logger = logger

    yield  # Application runs during this period

    # --- Shutdown ---
    app.state.database.dispose()

  app = FastAPI(lifespan=lifespan)
  app = __register_exception_handlers(app)
  app = __register_routes(app)
  return app

def __register_exception_handlers(app: FastAPI) -> FastAPI:
  register_400_bad_request_handlers(app, logger)
  register_404_not_found_handlers(app, logger)
  register_500_internal_server_error_handlers(app, logger)
  return app

def __register_routes(app: FastAPI) -> FastAPI:
  app.include_router(account_routes.router)
  app.include_router(blog_routes.router)
  app.include_router(health_routes.router)
  return app


if __name__ == "__main__":
  create_app()
