from urllib.parse import quote_plus

from sqlalchemy import Engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, SQLModel, create_engine, select, text

from domain.entities.account import Account
from infrastructure.base_infrastructure import Infrastructure
from infrastructure.database.exceptions.database_initialization_err import DatabaseInitializationErr
from infrastructure.database.exceptions.database_insert_err import DatabaseInsertErr
from infrastructure.database.exceptions.database_mapper_err import DatabaseMapperErr
from infrastructure.database.exceptions.database_multiple_matches_err import DatabaseMultipleMatchesErr
from infrastructure.database.exceptions.database_schema_creation_err import DatabaseSchemaCreationErr
from infrastructure.database.exceptions.database_select_err import DatabaseSelectErr
from infrastructure.database.mappers.account_orm_mapper import AccountMapper
from infrastructure.database.orm.account_orm import AccountORM
from shared.models.configs.database_config import DatabaseConfig
from shared.models.health_reports.database_health_report import DatabaseHealthReport


class Database(Infrastructure):
  _engine: Engine
  _session_factory: sessionmaker

  def __init__(self, database_config: DatabaseConfig):
    try:
      engine_str = database_config.engine
      if engine_str == "postgresql":
        engine_str = f"{engine_str}+psycopg"
      username = database_config.username
      password = quote_plus(database_config.password)
      host = database_config.host
      port = database_config.port
      name = database_config.name
      self._engine = create_engine(f"{engine_str}://{username}:{password}@{host}:{port}/{name}")
      self._session_factory = sessionmaker(bind=self._engine, future=True, expire_on_commit=False)
      if not getattr(self._engine, "_schema_initialized", False):
        self.create_schema()
        setattr(self._engine, "_schema_initialized", True)
      self._engine.connect().close()
      self.can_perform_basic_select()
      super().__init__()
    except Exception as e:
      raise DatabaseInitializationErr() from e

  def get_health_report(self) -> DatabaseHealthReport:
    can_perform_basic_select = self.can_perform_basic_select()
    is_engine = self.get_engine() is not None
    is_session_factory = self.get_session_factory() is not None
    healthy = can_perform_basic_select and is_engine and is_session_factory
    return DatabaseHealthReport(
      can_perform_basic_select=can_perform_basic_select,
      is_engine=is_engine,
      is_session_factory=is_session_factory,
      healthy=healthy
    )

  def get_session(self) -> Session:
    return Session(self._engine)

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
      SQLModel.metadata.create_all(self._engine)
    except SQLAlchemyError as e:
      raise DatabaseSchemaCreationErr() from e

  def dispose(self):
    self._engine.dispose()

  def get_uuid_from_account(
    self,
    account: Account
  ) -> str | None:
    try:
      with self.get_session() as session:
        stmt = select(AccountORM).where(
          AccountORM.name == account.get_name(),
          AccountORM.age == account.get_age(),
        )
        if account.get_uuid():
          stmt = stmt.where(AccountORM.uuid == account.get_uuid())
        results = session.exec(stmt).all()
    except SQLAlchemyError as e:
      raise DatabaseSelectErr() from e
    if not results:
      return None
    if len(results) > 1:
      raise DatabaseMultipleMatchesErr()
    uuid = results[0].uuid
    return uuid

  def get_account_from_uuid(
    self,
    uuid: str
  ) -> Account | None:
    try:
      with self.get_session() as session:
        stmt = select(AccountORM).where(
          AccountORM.uuid == uuid
        )
        first_account_orm_match = session.exec(stmt).first()
    except SQLAlchemyError as e:
      raise DatabaseSelectErr() from e
    if first_account_orm_match is None:
      return None
    account_match = AccountMapper.orm_to_domain(first_account_orm_match)
    return account_match

  def insert_account(
    self,
    account: Account
  ) -> Account:
    try:
      print(AccountORM.model_fields['timestamp'])
      account_orm = AccountMapper.domain_to_orm(account)
    except DatabaseMapperErr as e:
      raise DatabaseInsertErr() from e
    with self.get_session() as session:
      try:
        session.add(account_orm)   # "local load", nothing is executed in the DBMS yet
        session.flush()      # Create a transaction in the DBMS -- "load the DBMS"
        session.refresh(account_orm)  # Fetch the ORM from transaction -- give "account_orm" id/timestamp/etc
        session.commit()
      except SQLAlchemyError as e:
        session.rollback()
        raise DatabaseInsertErr() from e
      account = AccountMapper.orm_to_domain(account_orm)
      return account
