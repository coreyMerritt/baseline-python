from interfaces.rest.health.routes import health_routes
from interfaces.rest.models.projectname_fastapi import ProjectnameFastAPI
from interfaces.rest.v1.routes import account_routes, blog_routes


def register_routes(app: ProjectnameFastAPI) -> ProjectnameFastAPI:
  app.include_router(account_routes.router)
  app.include_router(blog_routes.router)
  app.include_router(health_routes.router)
  return app
