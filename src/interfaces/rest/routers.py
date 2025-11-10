#!/usr/bin/env python3
from fastapi import FastAPI

from interfaces.rest.v1.routes import account_routes
from interfaces.rest.v1.routes import blog_routes
from interfaces.rest.health.routes import health_routes


def create_app() -> FastAPI:
  app = FastAPI()
  app.include_router(account_routes.router)
  app.include_router(blog_routes.router)
  app.include_router(health_routes.router)
  return app

if __name__ == "__main__":
  create_app()
