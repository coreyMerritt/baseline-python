from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import select

from domain.entities.user import User
from domain.exceptions.repository_not_found_err import RepositoryNotFoundErr
from domain.exceptions.repository_unavailable_err import RepositoryUnavailableErr
from domain.interfaces.repositories.user_repository_interface import UserRepositoryInterface
from infrastructure.database.database import Database
from infrastructure.database.mappers.user_mapper import UserMapper
from infrastructure.database.orm.user_orm import UserORM


class UserRepository(UserRepositoryInterface):
  _database: Database

  def __init__(self, database: Database):
    self._database = database

  def get(self, uuid: str) -> User:
    try:
      with self._database.get_session() as session:
        stmt = select(UserORM).where(
          UserORM.uuid == uuid
        )
        first_user_orm_match = session.exec(stmt).first()
    except SQLAlchemyError as e:
      raise RepositoryUnavailableErr() from e
    if first_user_orm_match is None:
      raise RepositoryNotFoundErr()
    user_match = UserMapper.orm_to_domain(first_user_orm_match)
    return user_match

  def create(self, user: User) -> User:
    user_orm = UserMapper.domain_to_orm(user)
    with self._database.get_session() as session:
      try:
        session.add(user_orm)   # "local load", nothing is executed in the DBMS yet
        session.flush()      # Create a transaction in the DBMS -- "load the DBMS"
        session.refresh(user_orm)  # Fetch the ORM from transaction -- give "user_orm" id/timestamp/etc
        session.commit()
      except SQLAlchemyError as e:
        session.rollback()
        raise RepositoryUnavailableErr() from e
      user = UserMapper.orm_to_domain(user_orm)
      return user
