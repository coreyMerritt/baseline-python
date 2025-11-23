from interfaces.rest.types.projectname_fastapi import ProjectnameFastAPI


def shutdown(app: ProjectnameFastAPI) -> None:
  logger = app.infra.logger
  logger.debug("Shutting down webserver...")
  app.infra.database.dispose()
