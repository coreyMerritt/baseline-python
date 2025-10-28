from fastapi import APIRouter, HTTPException

from infrastructure.logging.log_manager import LogManager
from interfaces.rest.v1.controllers.account_controller import AccountController
from interfaces.rest.v1.dto.req.create_account_req import CreateAccountReq
from interfaces.rest.v1.dto.res.create_account_res import CreateAccountRes
from interfaces.rest.v1.dto.res.get_account_res import GetAccountRes

router = APIRouter(prefix="/api/v1")
controller = AccountController()
logger = LogManager.get_logger("AccountRoutes")

# NOTE: Most GETs will not use a Req, just one or more query params ex) /account?uuid=123
@router.get("/account", response_model=GetAccountRes)
async def get_account(uuid: str) -> GetAccountRes:
  try:
    return await controller.get_account(uuid)
  except HTTPException:
    raise
  except Exception as e:
    logger.critical("Unexpected non-HTTPException in routes", exc_info=e)
    raise HTTPException(status_code=500, detail="Internal server error") from e

@router.post("/account", response_model=CreateAccountRes)
async def create_account(req: CreateAccountReq) -> CreateAccountRes:
  try:
    return await controller.create_account(req)
  except HTTPException:
    raise
  except Exception as e:
    logger.critical("Unexpected non-HTTPException in routes", exc_info=e)
    raise HTTPException(status_code=500, detail="Internal server error") from e
