from interfaces.rest.models.foo_project_name_fastapi import FooProjectNameFastAPI


def shutdown(app: FooProjectNameFastAPI) -> None:
  logger = app.resources.infra.logger
  logger.info("Shutting down...")
  app.resources.infra.database.dispose()
