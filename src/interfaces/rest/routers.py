#!/usr/bin/env python3
from fastapi import FastAPI

from interfaces.rest.health.routes import health_routes
from interfaces.rest.v1.exceptions.handlers.exception import register_unhandled_exception_handler
from interfaces.rest.v1.routes import account_routes, blog_routes


def create_app() -> FastAPI:
  app = FastAPI()
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
