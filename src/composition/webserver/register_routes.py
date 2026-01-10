from interfaces.rest.health.routes import health_routes
from interfaces.rest.models.foo_project_name_fastapi import FooProjectNameFastAPI
from interfaces.rest.v1.routes import account_routes, authentication_routes, blog_routes


def register_routes(app: FooProjectNameFastAPI) -> FooProjectNameFastAPI:
  app.include_router(account_routes.router)
  app.include_router(authentication_routes.router)
  app.include_router(blog_routes.router)
  app.include_router(health_routes.router)
  return app
