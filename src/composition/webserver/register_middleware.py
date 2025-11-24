from interfaces.rest.middleware.request_id import RequestIDMiddleware
from interfaces.rest.types.projectname_fastapi import ProjectnameFastAPI


def register_middleware(app: ProjectnameFastAPI) -> ProjectnameFastAPI:
  app.add_middleware(RequestIDMiddleware)
  return app
