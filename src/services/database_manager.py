from logging import Logger

from domain.entities.account import Account
from infrastructure.database.database import Database, Session
from infrastructure.database.exceptions.database_schema_creation_exception import DatabaseSchemaCreationException
from services.abc_service import Service
from services.exceptions.database_creation_exception import DatabaseCreationException
from services.models.database_config import DatabaseConfig
from shared.models.health_reports.database_health_report import DatabaseHealthReport


class DatabaseManager(Service):
  _database: Database
  _logger: Logger

  def __init__(self, database_config: DatabaseConfig):
    super().__init__()
    c = database_config
    self._logger.debug(
      "Initializing %s engine for database %s: %s@%s:%s...",
      c.engine, c.name, c.username, c.host, c.port
    )
    try:
      self._database = Database(database_config)
    except DatabaseSchemaCreationException as e:
      raise DatabaseCreationException() from e

  def get_health_report(self) -> DatabaseHealthReport:
    can_perform_basic_select = self._database.can_perform_basic_select()
    is_engine = self._database.get_engine() is not None
    is_session_factory = self._database.get_session_factory() is not None
    healthy = can_perform_basic_select and is_engine and is_session_factory
    return DatabaseHealthReport(
      can_perform_basic_select=can_perform_basic_select,
      is_engine=is_engine,
      is_session_factory=is_session_factory,
      healthy=healthy
    )

  def get_session(self) -> Session:
    return self._database.get_session()

  def create_schema(self) -> None:
    self._logger.debug("Attempting to create database schema...")
    self._database.create_schema()
    self._logger.debug("Created database schema.")

  def dispose(self):
    self._database.dispose()

  def get_account_id(
    self,
    account: Account
  ) -> str | None:
    # Nothing useful to log here
    return self._database.get_uuid_from_account(account)

  def get_account(
    self,
    uuid: str
  ) -> Account | None:
    self._logger.debug("Attempting to retrieve account for uuid: %s", uuid)
    account = self._database.get_account_from_uuid(uuid)
    self._logger.debug("Successfully retrieved account for uuid: %s", uuid)
    return account

  def create_account(
    self,
    account: Account
  ) -> Account:
    return self._database.insert_account(account)
