#!/usr/bin/env python3
import traceback

from fastapi.concurrency import asynccontextmanager

from composition.webserver.register_exception_handlers import register_exception_handlers
from composition.webserver.register_middleware import register_middleware
from composition.webserver.register_routes import register_routes
from composition.webserver.shutdown import shutdown
from composition.webserver.startup import startup
from interfaces.rest.models.projectname_fastapi import ProjectnameFastAPI


def create_app( ) -> ProjectnameFastAPI:

  @asynccontextmanager
  async def lifespan(app: ProjectnameFastAPI):
    try:
      await startup(app)
      yield  # Application runs during this period
    except Exception as e:
      traceback.print_exc()
      raise e
    finally:
      shutdown(app)

  app = ProjectnameFastAPI()
  app = register_exception_handlers(app)
  app = register_middleware(app=app)
  app = register_routes(app)
  app.router.lifespan_context = lifespan
  return app


if __name__ == "__main__":
  create_app()
