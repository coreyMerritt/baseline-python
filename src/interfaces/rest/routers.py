from fastapi import FastAPI

from interfaces.rest.health.routes import health_routes
from interfaces.rest.v1.routes import account_routes


def create_app() -> FastAPI:
  app = FastAPI()
  app.include_router(health_routes.router)
  app.include_router(account_routes.router)
  return app
