from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import col, select

from domain.exceptions.repository_not_found_err import RepositoryNotFoundErr
from domain.exceptions.repository_unavailable_err import RepositoryUnavailableErr
from domain.interfaces.repositories.user_credential_repository_interface import UserCredentialRepositoryInterface
from infrastructure.auth.models.user_credential import UserCredential
from infrastructure.database.database import Database
from infrastructure.database.orm.user_credential_orm import UserCredentialORM


class UserCredentialRepository(UserCredentialRepositoryInterface):
  _database: Database

  def __init__(self, database: Database):
    self._database = database

  def get(self, user_ulid: str) -> UserCredential:
    try:
      with self._database.get_session() as session:
        statement = (
          select(UserCredentialORM)
          .where(col(UserCredentialORM.user_ulid) == user_ulid)
        )
        credential_orm = session.exec(statement).first()
    except SQLAlchemyError as e:
      raise RepositoryUnavailableErr() from e
    if credential_orm is None:
      raise RepositoryNotFoundErr()
    return UserCredential(
      user_ulid=credential_orm.user_ulid,
      password_hash=credential_orm.password_hash,
    )
