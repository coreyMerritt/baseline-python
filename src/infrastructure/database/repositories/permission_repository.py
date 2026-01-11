from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlmodel import col, delete, select, update

from domain.exceptions.repository_duplication_err import RepositoryDuplicationErr
from domain.exceptions.repository_not_found_err import RepositoryNotFoundErr
from domain.exceptions.repository_unavailable_err import RepositoryUnavailableErr
from domain.interfaces.repositories.permission_repository_interface import PermissionRepositoryInterface
from domain.subdomain.entities.permission import Permission
from infrastructure.database.database import Database
from infrastructure.database.mappers.permission_mapper import PermissionMapper
from infrastructure.database.orm.permission_orm import PermissionORM


class PermissionRepository(PermissionRepositoryInterface):
  _database: Database

  def __init__(self, database: Database):
    self._database = database

  def create(self, permission: Permission) -> Permission:
    permission_orm = PermissionMapper.domain_to_orm(permission)
    with self._database.get_session() as session:
      try:
        session.add(permission_orm)   # "local load", nothing is executed in the DBMS yet
        session.flush()      # Create a transaction in the DBMS -- "load the DBMS"
        session.refresh(permission_orm)  # Fetch the ORM from transaction -- give "permission_orm" id/timestamp/etc
        session.commit()
      except IntegrityError as e:
        session.rollback()
        if "unique constraint" in str(e):
          raise RepositoryDuplicationErr() from e
        raise RepositoryUnavailableErr() from e
      except SQLAlchemyError as e:
        session.rollback()
        raise RepositoryUnavailableErr() from e
      permission = PermissionMapper.orm_to_domain(permission_orm)
      return permission

  def get(self, ulid: str) -> Permission:
    try:
      with self._database.get_session() as session:
        select_statement = select(PermissionORM).where(
          col(PermissionORM.ulid) == ulid
        )
        first_permission_orm_match = session.exec(select_statement).first()
    except SQLAlchemyError as e:
      raise RepositoryUnavailableErr() from e
    if first_permission_orm_match is None:
      raise RepositoryNotFoundErr()
    permission_match = PermissionMapper.orm_to_domain(first_permission_orm_match)
    return permission_match

  def update(self, permission: Permission) -> Permission:
    try:
      with self._database.get_session() as session:
        update_statement = (
          update(PermissionORM)
          .where(col(PermissionORM.ulid) == permission.ulid)
          .values(
            key=permission.key
          )
        )
        result = session.exec(update_statement)
        if result.rowcount == 0:
          raise RepositoryNotFoundErr()
        select_statement = select(PermissionORM).where(
          col(PermissionORM.ulid) == permission.ulid
        )
        first_permission_orm_match = session.exec(select_statement).first()
    except SQLAlchemyError as e:
      raise RepositoryUnavailableErr() from e
    if first_permission_orm_match is None:
      raise RepositoryNotFoundErr()
    return PermissionMapper.orm_to_domain(first_permission_orm_match)

  def delete(self, ulid: str) -> Permission:
    permission = self.get(ulid)
    try:
      with self._database.get_session() as session:
        select_statement = delete(PermissionORM).where(
          col(PermissionORM.ulid) == ulid
        )
        session.exec(select_statement).first()
    except SQLAlchemyError as e:
      raise RepositoryUnavailableErr() from e
    return permission
