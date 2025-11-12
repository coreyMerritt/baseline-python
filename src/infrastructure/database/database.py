from urllib.parse import quote_plus

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker

from domain.entities.account import Account
from infrastructure.abc_infrastructure import Infrastructure
from infrastructure.database.base import Base
from infrastructure.database.exceptions.database_engine_creation_exception import DatabaseEngineCreationException
from infrastructure.database.exceptions.database_enum_mapping_exception import DatabaseEnumMappingException
from infrastructure.database.exceptions.database_insert_exception import DatabaseInsertException
from infrastructure.database.exceptions.database_multiple_matches_exception import DatabaseMultipleMatchesException
from infrastructure.database.exceptions.database_schema_creation_exception import DatabaseSchemaCreationException
from infrastructure.database.exceptions.database_select_exception import DatabaseSelectException
from infrastructure.database.mappers.account_orm_mapper import AccountMapper
from infrastructure.database.orm.account_orm import AccountORM
from services.models.database_config import DatabaseConfig


class Database(Infrastructure):
  _engine: Engine
  _session_factory: sessionmaker

  def __init__(self, database_config: DatabaseConfig):
    engine_str = database_config.engine
    if engine_str == "postgresql":
      engine_str = f"{engine_str}+psycopg"
    username = database_config.username
    password = quote_plus(database_config.password)
    host = database_config.host
    port = database_config.port
    name = database_config.name
    try:
      self._engine = create_engine(f"{engine_str}://{username}:{password}@{host}:{port}/{name}")
    except SQLAlchemyError as e:
      raise DatabaseEngineCreationException(str(e)) from e
    self._session_factory = sessionmaker(bind=self._engine, future=True, expire_on_commit=False)
    if not getattr(self._engine, "_schema_initialized", False):
      self.create_schema()
      setattr(self._engine, "_schema_initialized", True)
    self._engine.connect().close()

  def get_session(self) -> Session:
    return self._session_factory()

  def get_session_factory(self) -> sessionmaker:
    return self._session_factory

  def get_engine(self) -> Engine:
    return self._engine

  def can_perform_basic_select(self) -> bool:
    try:
      with self._engine.connect() as conn:
        conn.execute(text("SELECT 1"))
      return True
    except SQLAlchemyError:
      return False


  def create_schema(self) -> None:
    try:
      Base.metadata.create_all(self._engine)
    except SQLAlchemyError as e:
      raise DatabaseSchemaCreationException(str(e)) from e

  def dispose(self):
    self._engine.dispose()

  def get_uuid_from_account(
    self,
    account: Account
  ) -> str | None:
    # NOTE: We don't do a logging/debug here because we can't give good info on the account without breaking privacy
    try:
      with self.get_session() as session:
        query = (
          # NOTE: We use filter_by(...) with slightly different formatting for multiple filter situations
          session.query(AccountORM).filter_by(
            name=account.get_name(),
            age=account.get_age()
          )
        )
        if account.get_uid():
          query = query.filter(AccountORM.uuid == account.get_uid())
        results = query.all()
    except SQLAlchemyError as e:
      raise DatabaseSelectException(str(e)) from e
    # Handling this inside the session is important because of lazy loading? Hmmm
    if not results:
      return None
    if len(results) > 1:
      raise DatabaseMultipleMatchesException()
    uuid = results[0].uuid
    return uuid

  def get_account_from_uuid(
    self,
    uuid: str
  ) -> Account | None:
    try:
      with self.get_session() as session:
        first_account_orm_match = (
          session.query(AccountORM)
          # NOTE: we use filter(...) for single filter situations
          .filter(AccountORM.uuid == uuid)
          .first()
        )
    except SQLAlchemyError as e:
      raise DatabaseSelectException(str(e)) from e
    # Handling this inside the session is important because of lazy loading? Hmmm
    if first_account_orm_match is None:
      return None
    try:
      account_match = AccountMapper.orm_to_domain(first_account_orm_match)
    except DatabaseEnumMappingException as e:
      raise DatabaseSelectException(str(e)) from e
    return account_match

  def insert_account(
    self,
    account: Account
  ) -> Account:
    try:
      account_orm = AccountMapper.domain_to_orm(account)
    except DatabaseEnumMappingException as e:
      raise DatabaseInsertException(str(e)) from e
    with self.get_session() as session:
      try:
        session.add(account_orm)   # "local load", nothing is executed in the DBMS yet
        session.flush()      # Create a transaction in the DBMS -- "load the DBMS"
        session.refresh(account_orm)  # Fetch the ORM from transaction -- give "account_orm" id/timestamp/etc
        session.commit()
      # We always use try/except when writing to databases for safety
      except SQLAlchemyError as e:
        session.rollback()
        raise DatabaseInsertException(str(e)) from e
      account = AccountMapper.orm_to_domain(account_orm)
      return account
