#!/usr/bin/env python3
from types import SimpleNamespace

from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager

from interfaces.rest.exceptions.handlers._400_bad_request import register_400_bad_request_handlers
from interfaces.rest.exceptions.handlers._404_not_found import register_404_not_found_handlers
from interfaces.rest.exceptions.handlers._500_internal_server_error import register_500_internal_server_error_handlers
from interfaces.rest.health.routes import health_routes
from interfaces.rest.v1.routes import account_routes, blog_routes
from shared.shared_infrastructure import (DEPLOYMENT_ENV, account_repository, blog_post_repository, config_parser, cpu,
                                          database, disk, environment, logger, memory, typicode_client)


def create_app() -> FastAPI:
  @asynccontextmanager
  async def lifespan(app: FastAPI):
    # --- Startup ---
    logger.debug(f"Using deployment environment: {DEPLOYMENT_ENV}")
    ## Infra
    infra = SimpleNamespace()
    infra.config_parser = config_parser
    infra.cpu = cpu
    infra.database = database
    infra.disk = disk
    infra.environment = environment
    infra.logger = logger
    infra.memory = memory
    infra.typicode_client = typicode_client
    ## Repositories
    repo = SimpleNamespace()
    repo.account = account_repository
    repo.blog_post = blog_post_repository
    ## Namespace assignments
    app.state.infra = infra
    app.state.repo = repo

    yield  # Application runs during this period

    # --- Shutdown ---
    app.state.infra.database.dispose()

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
