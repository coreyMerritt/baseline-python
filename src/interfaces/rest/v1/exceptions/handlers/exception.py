from fastapi import FastAPI, HTTPException, Request

from infrastructure.logging.log_manager import LogManager


def register_unhandled_exception_handler(app: FastAPI) -> None:
  logger = LogManager.get_logger("Unhandled Exception Handler")
  @app.exception_handler(Exception)
  async def handle_unhandled_exception(r: Request, e: Exception):
    _ = r
    logger.error("Caught Unhandled Exception", exc_info=e)
    raise HTTPException(status_code=500, detail="Internal server error") from e
