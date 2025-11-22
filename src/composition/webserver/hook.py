#!/usr/bin/env python3
from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager

from composition.webserver.register_exception_handlers import register_exception_handlers
from composition.webserver.register_routes import register_routes
from composition.webserver.shutdown import shutdown
from composition.webserver.startup import startup


def create_app() -> FastAPI:
  @asynccontextmanager
  async def lifespan(app: FastAPI):
    startup(app)
    yield  # Application runs during this period
    shutdown(app)

  app = FastAPI(lifespan=lifespan)
  app = register_exception_handlers(app)
  app = register_routes(app)
  return app


if __name__ == "__main__":
  create_app()
