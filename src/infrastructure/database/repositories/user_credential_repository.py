from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlmodel import col, delete, select, update

from domain.exceptions.repository_duplication_err import RepositoryDuplicationErr
from domain.exceptions.repository_not_found_err import RepositoryNotFoundErr
from domain.exceptions.repository_unavailable_err import RepositoryUnavailableErr
from domain.interfaces.repositories.user_credential_repository_interface import UserCredentialRepositoryInterface
from infrastructure.auth.models.user_credential import UserCredential
from infrastructure.database.database import Database
from infrastructure.database.mappers.user_credential_mapper import UserCredentialMapper
from infrastructure.database.orm.user_credential_orm import UserCredentialORM


class UserCredentialRepository(UserCredentialRepositoryInterface):
  _database: Database

  def __init__(self, database: Database):
    self._database = database

  def create(self, user_credential: UserCredential) -> UserCredential:
    user_credential_orm = UserCredentialMapper.model_to_orm(user_credential)
    with self._database.get_session() as session:
      try:
        session.add(user_credential_orm)   # "local load", nothing is executed in the DBMS yet
        session.flush()      # Create a transaction in the DBMS -- "load the DBMS"
        session.refresh(user_credential_orm)  # Fetch the ORM from transaction -- give "user_credential_orm" id/timestamp/etc
        session.commit()
      except IntegrityError as e:
        session.rollback()
        if "unique constraint" in str(e):
          raise RepositoryDuplicationErr() from e
        raise RepositoryUnavailableErr() from e
      except SQLAlchemyError as e:
        session.rollback()
        raise RepositoryUnavailableErr() from e
      user_credential = UserCredentialMapper.orm_to_model(user_credential_orm)
      return user_credential

  def get(self, user_ulid: str) -> UserCredential:
    try:
      with self._database.get_session() as session:
        select_statement = select(UserCredentialORM).where(
          col(UserCredentialORM.user_ulid) == user_ulid
        )
        first_user_credential_orm_match = session.exec(select_statement).first()
    except SQLAlchemyError as e:
      raise RepositoryUnavailableErr() from e
    if first_user_credential_orm_match is None:
      raise RepositoryNotFoundErr()
    user_credential_match = UserCredentialMapper.orm_to_model(first_user_credential_orm_match)
    return user_credential_match

  def update(self, user_credential: UserCredential) -> UserCredential:
    try:
      with self._database.get_session() as session:
        update_statement = (
          update(UserCredentialORM)
          .where(col(UserCredentialORM.user_ulid) == user_credential.user_ulid)
          .values(
            password_hash=user_credential.password_hash
          )
        )
        result = session.exec(update_statement)
        if result.rowcount == 0:
          raise RepositoryNotFoundErr()
        select_statement = select(UserCredentialORM).where(
          col(UserCredentialORM.user_ulid) == user_credential.user_ulid
        )
        first_user_credential_orm_match = session.exec(select_statement).first()
    except SQLAlchemyError as e:
      raise RepositoryUnavailableErr() from e
    if first_user_credential_orm_match is None:
      raise RepositoryNotFoundErr()
    user_credential_match = UserCredentialMapper.orm_to_model(first_user_credential_orm_match)
    return user_credential_match

  def delete(self, user_ulid: str) -> UserCredential:
    user_credential = self.get(user_ulid)
    try:
      with self._database.get_session() as session:
        select_statement = delete(UserCredentialORM).where(
          col(UserCredentialORM.user_ulid) == user_ulid
        )
        session.exec(select_statement).first()
    except SQLAlchemyError as e:
      raise RepositoryUnavailableErr() from e
    return user_credential
