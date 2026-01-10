from datetime import datetime, UTC

import hashlib
import hmac

from sqlmodel import select

from domain.interfaces.authenticator import AuthenticatorInterface
from infrastructure.auth.exceptions.token_expired_err import TokenExpiredErr
from infrastructure.auth.exceptions.token_not_found_err import TokenNotFoundErr
from infrastructure.auth.exceptions.token_revoked_err import TokenRevokedErr
from infrastructure.auth.models.authenticator_config import AuthenticatorConfig
from infrastructure.database.database import Database
from infrastructure.database.orm.auth_token_orm import AuthTokenORM


class Authenticator(AuthenticatorInterface):
  _secret: str
  _database: Database

  def __init__(self, authenticator_config: AuthenticatorConfig, database: Database):
    self._secret = authenticator_config.secret
    self._database = database

  def authenticate(self, token: str) -> str:
    token_hash = self._hash_token(token)
    with self._database.get_session() as session:
      statement = (
        select(AuthTokenORM)
        .where(AuthTokenORM.token_hash == token_hash)
      )
      auth_token = session.exec(statement).one_or_none()
    if auth_token is None:
      raise TokenNotFoundErr()
    if auth_token.revoked_at is not None:
      raise TokenRevokedErr()
    if auth_token.expires_at is not None and auth_token.expires_at < datetime.now(tz=UTC):
      raise TokenExpiredErr()
    return auth_token.user_ulid

  def _hash_token(self, token: str) -> str:
    if not token:
      raise ValueError("Token must not be empty")
    return hmac.new(
      key=self._secret.encode("utf-8"),
      msg=token.encode("utf-8"),
      digestmod=hashlib.sha256,
    ).hexdigest()
