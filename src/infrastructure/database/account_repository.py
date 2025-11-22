from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import select

from domain.entities.account import Account
from domain.exceptions.repository_not_found_err import RepositoryNotFoundErr
from domain.exceptions.repository_unavailable_err import RepositoryUnavailableErr
from domain.interfaces.repositories.account_repository_interface import AccountRepositoryInterface
from infrastructure.database.database import Database
from infrastructure.database.mappers.account_mapper import AccountMapper
from infrastructure.database.orm.account_orm import AccountORM


class AccountRepository(AccountRepositoryInterface):
  _database: Database

  def __init__(self, database: Database):
    self._database = database

  def get(self, uuid: str) -> Account:
    try:
      with self._database.get_session() as session:
        stmt = select(AccountORM).where(
          AccountORM.uuid == uuid
        )
        first_account_orm_match = session.exec(stmt).first()
    except SQLAlchemyError as e:
      raise RepositoryUnavailableErr() from e
    if first_account_orm_match is None:
      raise RepositoryNotFoundErr()
    account_match = AccountMapper.orm_to_domain(first_account_orm_match)
    return account_match

  def insert(self, account: Account) -> Account:
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
