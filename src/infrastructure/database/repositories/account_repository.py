from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import col, delete, select, update

from domain.exceptions.repository_not_found_err import RepositoryNotFoundErr
from domain.exceptions.repository_unavailable_err import RepositoryUnavailableErr
from domain.interfaces.repositories.account_repository_interface import AccountRepositoryInterface
from domain.subdomain.entities.account import Account
from infrastructure.database.database import Database
from infrastructure.database.mappers.account_mapper import AccountMapper
from infrastructure.database.orm.account_orm import AccountORM


class AccountRepository(AccountRepositoryInterface):
  _database: Database

  def __init__(self, database: Database):
    self._database = database

  def create(self, account: Account) -> Account:
    account_orm = AccountMapper.domain_to_orm(account)
    with self._database.get_session() as session:
      try:
        session.add(account_orm)   # "local load", nothing is executed in the DBMS yet
        session.flush()      # Create a transaction in the DBMS -- "load the DBMS"
        session.refresh(account_orm)  # Fetch the ORM from transaction -- give "account_orm" id/timestamp/etc
        session.commit()
      except SQLAlchemyError as e:
        session.rollback()
        raise RepositoryUnavailableErr() from e
      account = AccountMapper.orm_to_domain(account_orm)
      return account

  def get(self, ulid: str) -> Account:
    try:
      with self._database.get_session() as session:
        select_statement = select(AccountORM).where(
          col(AccountORM.ulid) == ulid
        )
        first_account_orm_match = session.exec(select_statement).first()
    except SQLAlchemyError as e:
      raise RepositoryUnavailableErr() from e
    if first_account_orm_match is None:
      raise RepositoryNotFoundErr()
    account_match = AccountMapper.orm_to_domain(first_account_orm_match)
    return account_match

  def update(self, account: Account) -> Account:
    try:
      with self._database.get_session() as session:
        update_statement = (
          update(AccountORM)
          .where(col(AccountORM.ulid) == account.ulid)
          .values(
            name=account.name,
            status=account.status.value,
            suspended_at=account.suspended_at,
            deleted_at=account.deleted_at
          )
        )
        result = session.exec(update_statement)
        if result.rowcount == 0:
          raise RepositoryNotFoundErr()
        select_statement = select(AccountORM).where(
          col(AccountORM.ulid) == account.ulid
        )
        first_account_orm_match = session.exec(select_statement).first()
    except SQLAlchemyError as e:
      raise RepositoryUnavailableErr() from e
    if first_account_orm_match is None:
      raise RepositoryNotFoundErr()
    return AccountMapper.orm_to_domain(first_account_orm_match)

  def delete(self, ulid: str) -> Account:
    account = self.get(ulid)
    try:
      with self._database.get_session() as session:
        select_statement = delete(AccountORM).where(
          col(AccountORM.ulid) == ulid
        )
        session.exec(select_statement)
    except SQLAlchemyError as e:
      raise RepositoryUnavailableErr() from e
    return account
