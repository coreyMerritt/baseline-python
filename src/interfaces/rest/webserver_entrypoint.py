#!/usr/bin/env python3
from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager

from infrastructure.database.exceptions.database_schema_creation_exception import DatabaseSchemaCreationException
from interfaces.rest.exceptions.app_initialization_exception import AppInitializationException
from interfaces.rest.health.routes import health_routes
from interfaces.rest.v1.exceptions.handlers.exception import register_unhandled_exception_handler
from interfaces.rest.v1.routes import account_routes, blog_routes
from services.config_manager import ConfigManager
from services.database_manager import DatabaseManager


def create_app() -> FastAPI:
  @asynccontextmanager
  async def lifespan(app: FastAPI):
    # --- Startup ---
    ConfigManager.refresh()

    # Initialize shared database manager once
    database_config = ConfigManager.get_database_config()
    try:
      app.state.db = DatabaseManager(database_config)
    except DatabaseSchemaCreationException as e:
      raise AppInitializationException(
        "Database schema creation failed.",
        {"config_dir": ConfigManager.get_config_dir()}
      ) from e

    yield  # Application runs during this period

    # --- Shutdown ---
    app.state.db.dispose()

  app = FastAPI(lifespan=lifespan)
  app = __register_exception_handlers(app)
  app = __register_routes(app)
  return app

def __register_exception_handlers(app: FastAPI) -> FastAPI:
  register_unhandled_exception_handler(app)
  return app

def __register_routes(app: FastAPI) -> FastAPI:
  app.include_router(account_routes.router)
  app.include_router(blog_routes.router)
  app.include_router(health_routes.router)
  return app


if __name__ == "__main__":
  create_app()
