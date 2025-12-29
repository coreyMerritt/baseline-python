from interfaces.rest.models.projectname_fastapi import ProjectnameFastAPI


def shutdown(app: ProjectnameFastAPI) -> None:
  logger = app.infra.logger
  logger.info("Shutting down...")
  app.infra.database.dispose()
