#!/usr/bin/env python3
from fastapi.concurrency import asynccontextmanager

from composition.webserver.register_exception_handlers import register_exception_handlers
from composition.webserver.register_middleware import register_middleware
from composition.webserver.register_routes import register_routes
from composition.webserver.shutdown import shutdown
from composition.webserver.startup import startup
from interfaces.rest.types.projectname_fastapi import ProjectnameFastAPI


def create_app() -> ProjectnameFastAPI:
  @asynccontextmanager
  async def lifespan(app: ProjectnameFastAPI):
    startup(app)
    yield  # Application runs during this period
    shutdown(app)

  app = ProjectnameFastAPI(lifespan=lifespan)
  app = register_exception_handlers(app)
  app = register_middleware(app)
  app = register_routes(app)
  return app


if __name__ == "__main__":
  create_app()
