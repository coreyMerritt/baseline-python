from typing import Callable
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from domain.interfaces.authenticator import AuthenticatorInterface
from infrastructure.auth.exceptions.token_expired_err import TokenExpiredErr
from infrastructure.auth.exceptions.token_not_found_err import TokenNotFoundErr
from infrastructure.auth.exceptions.token_revoked_err import TokenRevokedErr
from infrastructure.types.logger_interface import LoggerInterface


class AuthMiddleware(BaseHTTPMiddleware):
  _get_authenticator: Callable[[], AuthenticatorInterface]
  _get_logger: Callable[[], LoggerInterface]

  def __init__(
    self,
    app,
    get_authenticator: Callable[[], AuthenticatorInterface],
    get_logger: Callable[[], LoggerInterface]
  ):
    self._get_authenticator = get_authenticator
    self._get_logger = get_logger
    super().__init__(app)

  async def dispatch(self, request: Request, call_next):
    logger = self._get_logger()
    authenticator = self._get_authenticator()
    request.state.is_authenticated = False
    request.state.user_ulid = None
    auth_header = request.headers.get("Authorization")
    if auth_header is None:
      return await call_next(request)
    if not auth_header.startswith("Bearer "):
      return JSONResponse(
        status_code=401,
        content={
          "data": None,
          "error": {
            "message": "Unauthorized1"
          }
        }
      )
    token = auth_header.removeprefix("Bearer ").strip()
    try:
      logger.debug("Attemping to authenticate...")
      user_ulid = authenticator.authenticate(token)
      request.state.is_authenticated = True
      request.state.user_ulid = user_ulid
      logger.info("Authentication Successful")
    except (
      TokenNotFoundErr,
      TokenRevokedErr,
      TokenExpiredErr,
    ) as e:
      return JSONResponse(
        status_code=401,
        content={
          "data": None,
          "error": {
            "message": f"Unauthorized: {e}"
          }
        }
      )
    return await call_next(request)
