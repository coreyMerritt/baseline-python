from logging import Logger
from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker

from domain.entities.account import Account
from infrastructure.config.models.database_config import DatabaseConfig
from infrastructure.database.base import Base
from infrastructure.database.exceptions.database_engine_creation_exception import DatabaseEngineCreationException
from infrastructure.database.exceptions.database_enum_mapping_exception import DatabaseEnumMappingException
from infrastructure.database.exceptions.database_insert_exception import DatabaseInsertException
from infrastructure.database.exceptions.database_multiple_matches_exception import DatabaseMultipleMatchesException
from infrastructure.database.exceptions.database_schema_creation_exception import DatabaseSchemaCreationException
from infrastructure.database.exceptions.database_select_exception import DatabaseSelectException
from infrastructure.database.mappers.account_orm_mapper import AccountMapper
from infrastructure.database.orm.account_orm import AccountORM
from infrastructure.logging.log_manager import LogManager


class DatabaseManager:
  _logger: Logger
  _first_instantiation: bool = True
  _engine: Engine
  _session_factory: sessionmaker

  def __init__(self, database_config: DatabaseConfig):
    self._logger = LogManager.get_logger(self.__class__.__name__)
    engine = database_config.engine
    if engine == "postgresql":
      engine = f"{engine}+psycopg"
    username = database_config.username
    password = quote_plus(database_config.password)
    host = database_config.host
    port = database_config.port
    name = database_config.name
    self._logger.debug(
      "Initializing %s engine for database %s: %s@%s:%s...",
      engine, name, username, host, port
    )
    try:
      self._engine = create_engine(f"{engine}://{username}:{password}@{host}:{port}/{name}")
      self._logger.debug(
        "Initialized %s engine for database %s: %s@%s:%s",
        engine, name, username, host, port
      )
    except SQLAlchemyError as e:
      raise DatabaseEngineCreationException() from e
    self._session_factory = sessionmaker(bind=self._engine, future=True, expire_on_commit=False)
    if DatabaseManager._first_instantiation:
      self.create_schema()
      DatabaseManager._first_instantiation = False


  def create_schema(self) -> None:
    self._logger.debug("Attempting to create database schema...")
    try:
      Base.metadata.create_all(self._engine)
      self._logger.debug("Created database schema.")
    except SQLAlchemyError as e:
      raise DatabaseSchemaCreationException() from e

  def get_session(self) -> Session:
    return self._session_factory()

  def get_id_from_account(
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
      raise DatabaseSelectException() from e
    # Handling this inside the session is important because of lazy loading? Hmmm
    if not results:
      return None
    if len(results) > 1:
      raise DatabaseMultipleMatchesException()
    uuid = results[0].uuid
    return uuid

  def get_account_from_id(
    self,
    uuid: str
  ) -> Account | None:
    self._logger.debug("Attempting to retrieve account for uuid: %s", uuid)
    try:
      with self.get_session() as session:
        first_account_orm_match = (
          session.query(AccountORM)
          # NOTE: we use filter(...) for single filter situations
          .filter(AccountORM.uuid == uuid)
          .first()
        )
      self._logger.debug("Retrieved account for uuid: %s", uuid)
    except SQLAlchemyError as e:
      raise DatabaseSelectException() from e
    # Handling this inside the session is important because of lazy loading? Hmmm
    if first_account_orm_match is None:
      return None
    try:
      account_match = AccountMapper.orm_to_domain(first_account_orm_match)
    except DatabaseEnumMappingException as e:
      raise DatabaseSelectException() from e
    return account_match

  def create_account(
    self,
    account: Account
  ) -> Account:
    try:
      account_orm = AccountMapper.domain_to_orm(account)
    except DatabaseEnumMappingException as e:
      raise DatabaseInsertException() from e
    with self.get_session() as session:
      try:
        session.add(account_orm)   # "local load", nothing is executed in the DBMS yet
        session.flush()      # Create a transaction in the DBMS -- "load the DBMS"
        session.refresh(account_orm)  # Fetch the ORM from transaction -- give "account_orm" id/timestamp/etc
        session.commit()
      # We always use try/except when writing to databases for safety
      except SQLAlchemyError as e:
        session.rollback()
        raise DatabaseInsertException() from e
      account = AccountMapper.orm_to_domain(account_orm)
      return account
