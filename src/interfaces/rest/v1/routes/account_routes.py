from fastapi import APIRouter, HTTPException

from infrastructure.logging.log_manager import LogManager
from interfaces.rest.v1.controllers.account_controller import AccountController
from interfaces.rest.v1.dto.req.create_account_req import CreateAccountReq
from interfaces.rest.v1.dto.res.create_account_res import CreateAccountRes
from interfaces.rest.v1.dto.res.get_account_res import GetAccountRes

router = APIRouter(prefix="/api/v1/account")
controller = AccountController()
logger = LogManager.get_logger("AccountRoutes")

# NOTE: Most GETs will not use a Req, just one or more query params ex) /account?uuid=123
@router.get(
  path="/",
  response_model=GetAccountRes,
  status_code=200
)
async def get_account(uuid: str) -> GetAccountRes:
  try:
    return await controller.get_account(uuid)
  except HTTPException:
    raise
  except Exception as e:
    logger.critical("Unexpected non-HTTPException in routes", exc_info=e)
    raise HTTPException(status_code=500, detail="Internal server error") from e

@router.post(
  path="/",
  response_model=CreateAccountRes,
  status_code=201
)
async def create_account(req: CreateAccountReq) -> CreateAccountRes:
  try:
    return await controller.create_account(req)
  except HTTPException:
    raise
  except Exception as e:
    logger.critical("Unexpected non-HTTPException in routes", exc_info=e)
    raise HTTPException(status_code=500, detail="Internal server error") from e
