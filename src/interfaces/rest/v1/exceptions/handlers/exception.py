from fastapi import FastAPI, HTTPException, Request

from infrastructure.logging.projectname_logger import ProjectnameLogger


def register_unhandled_exception_handler(app: FastAPI) -> None:
  @app.exception_handler(Exception)
  async def handle_unhandled_exception(r: Request, e: Exception):
    _ = r
    logger = ProjectnameLogger.get_logger("Unhandled Exception Handler")
    logger.error("Caught Unhandled Exception", exc_info=e)
    raise HTTPException(status_code=500, detail="Internal server error") from e
