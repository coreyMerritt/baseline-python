from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlmodel import col, delete, select, update

from domain.exceptions.repository_duplication_err import RepositoryDuplicationErr
from domain.exceptions.repository_not_found_err import RepositoryNotFoundErr
from domain.exceptions.repository_unavailable_err import RepositoryUnavailableErr
from domain.interfaces.repositories.role_repository_interface import RoleRepositoryInterface
from domain.subdomain.entities.role import Role
from infrastructure.database.database import Database
from infrastructure.database.mappers.role_mapper import RoleMapper
from infrastructure.database.orm.role_orm import RoleORM


class RoleRepository(RoleRepositoryInterface):
  _database: Database

  def __init__(self, database: Database):
    self._database = database

  def create(self, role: Role) -> Role:
    role_orm = RoleMapper.domain_to_orm(role)
    with self._database.get_session() as session:
      try:
        session.add(role_orm)   # "local load", nothing is executed in the DBMS yet
        session.flush()      # Create a transaction in the DBMS -- "load the DBMS"
        session.refresh(role_orm)  # Fetch the ORM from transaction -- give "role_orm" id/timestamp/etc
        session.commit()
      except IntegrityError as e:
        session.rollback()
        if "unique constraint" in str(e):
          raise RepositoryDuplicationErr() from e
        raise RepositoryUnavailableErr() from e
      except SQLAlchemyError as e:
        session.rollback()
        raise RepositoryUnavailableErr() from e
      role = RoleMapper.orm_to_domain(role_orm)
      return role

  def exists_by_name(self, name: str) -> bool:
    try:
      with self._database.get_session() as session:
        select_statement = select(RoleORM).where(
          col(RoleORM.name) == name
        )
        first_role_orm_match = session.exec(select_statement).first()
    except SQLAlchemyError as e:
      raise RepositoryUnavailableErr() from e
    if first_role_orm_match is None:
      return False
    return True

  def get(self, ulid: str) -> Role:
    try:
      with self._database.get_session() as session:
        select_statement = select(RoleORM).where(
          col(RoleORM.ulid) == ulid
        )
        first_role_orm_match = session.exec(select_statement).first()
    except SQLAlchemyError as e:
      raise RepositoryUnavailableErr() from e
    if first_role_orm_match is None:
      raise RepositoryNotFoundErr()
    role_match = RoleMapper.orm_to_domain(first_role_orm_match)
    return role_match

  def get_by_name(self, name: str) -> Role:
    try:
      with self._database.get_session() as session:
        select_statement = select(RoleORM).where(
          col(RoleORM.name) == name
        )
        first_role_orm_match = session.exec(select_statement).first()
    except SQLAlchemyError as e:
      raise RepositoryUnavailableErr() from e
    if first_role_orm_match is None:
      raise RepositoryNotFoundErr()
    role_match = RoleMapper.orm_to_domain(first_role_orm_match)
    return role_match

  def update(self, role: Role) -> Role:
    try:
      with self._database.get_session() as session:
        update_statement = (
          update(RoleORM)
          .where(col(RoleORM.ulid) == role.ulid)
          .values(
            name=role.name
          )
        )
        result = session.exec(update_statement)
        if result.rowcount == 0:
          raise RepositoryNotFoundErr()
        select_statement = select(RoleORM).where(
          col(RoleORM.ulid) == role.ulid
        )
        first_role_orm_match = session.exec(select_statement).first()
    except SQLAlchemyError as e:
      raise RepositoryUnavailableErr() from e
    if first_role_orm_match is None:
      raise RepositoryNotFoundErr()
    return RoleMapper.orm_to_domain(first_role_orm_match)

  def delete(self, ulid: str) -> Role:
    role = self.get(ulid)
    try:
      with self._database.get_session() as session:
        select_statement = delete(RoleORM).where(
          col(RoleORM.ulid) == ulid
        )
        session.exec(select_statement).first()
    except SQLAlchemyError as e:
      raise RepositoryUnavailableErr() from e
    return role
