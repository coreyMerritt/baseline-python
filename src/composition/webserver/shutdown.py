from fastapi import FastAPI


def shutdown(app: FastAPI) -> None:
  logger = app.state.infra.logger
  logger.debug("Shutting down webserver...")
  app.state.infra.database.dispose()
