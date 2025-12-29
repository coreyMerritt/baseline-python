from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import col, delete, select, update

from domain.exceptions.repository_not_found_err import RepositoryNotFoundErr
from domain.exceptions.repository_unavailable_err import RepositoryUnavailableErr
from domain.interfaces.repositories.membership_repository_interface import MembershipRepositoryInterface
from domain.subdomain.entities.membership import Membership
from infrastructure.database.database import Database
from infrastructure.database.mappers.membership_mapper import MembershipMapper
from infrastructure.database.orm.membership_orm import MembershipORM


class MembershipRepository(MembershipRepositoryInterface):
  _database: Database

  def __init__(self, database: Database):
    self._database = database

  def create(self, membership: Membership) -> Membership:
    membership_orm = MembershipMapper.domain_to_orm(membership)
    with self._database.get_session() as session:
      try:
        session.add(membership_orm)   # "local load", nothing is executed in the DBMS yet
        session.flush()      # Create a transaction in the DBMS -- "load the DBMS"
        session.refresh(membership_orm)  # Fetch the ORM from transaction -- give "membership_orm" id/timestamp/etc
        session.commit()
      except SQLAlchemyError as e:
        session.rollback()
        raise RepositoryUnavailableErr() from e
      membership = MembershipMapper.orm_to_domain(membership_orm)
      return membership

  def get(self, ulid: str) -> Membership:
    try:
      with self._database.get_session() as session:
        select_statement = select(MembershipORM).where(
          col(MembershipORM.ulid) == ulid
        )
        first_membership_orm_match = session.exec(select_statement).first()
    except SQLAlchemyError as e:
      raise RepositoryUnavailableErr() from e
    if first_membership_orm_match is None:
      raise RepositoryNotFoundErr()
    membership_match = MembershipMapper.orm_to_domain(first_membership_orm_match)
    return membership_match

  def update(self, membership: Membership) -> Membership:
    try:
      with self._database.get_session() as session:
        update_statement = (
          update(MembershipORM)
          .where(col(MembershipORM.ulid) == membership.ulid)
          .values(
            status=membership.status.value,
            joined_at=membership.joined_at,
            removed_at=membership.removed_at
          )
        )
        result = session.exec(update_statement)
        if result.rowcount == 0:
          raise RepositoryNotFoundErr()
        select_statement = select(MembershipORM).where(
          col(MembershipORM.ulid) == membership.ulid
        )
        first_membership_orm_match = session.exec(select_statement).first()
    except SQLAlchemyError as e:
      raise RepositoryUnavailableErr() from e
    if first_membership_orm_match is None:
      raise RepositoryNotFoundErr()
    return MembershipMapper.orm_to_domain(first_membership_orm_match)

  def delete(self, ulid: str) -> Membership:
    membership = self.get(ulid)
    try:
      with self._database.get_session() as session:
        select_statement = delete(MembershipORM).where(
          col(MembershipORM.ulid) == ulid
        )
        session.exec(select_statement).first()
    except SQLAlchemyError as e:
      raise RepositoryUnavailableErr() from e
    return membership
