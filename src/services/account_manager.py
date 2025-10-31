from logging import Logger

from domain.entities.account import Account
from domain.enums.account_type import AccountType
from domain.exceptions.domain_validation_exception import DomainValidationException
from infrastructure.config.config_manager import ConfigManager
from infrastructure.database.database_manager import DatabaseManager
from infrastructure.database.exceptions.database_schema_creation_exception import DatabaseSchemaCreationException
from infrastructure.database.exceptions.database_select_exception import DatabaseSelectException
from infrastructure.logging.log_manager import LogManager
from services.exceptions.data_exception import DataException
from services.exceptions.data_validation_exception import DataValidationException


class AccountManager:
  _database_manager: DatabaseManager
  _logger: Logger

  def __init__(self):
    database_config = ConfigManager.get_database_config()
    try:
      self._database_manager = DatabaseManager(database_config)
    except DatabaseSchemaCreationException as e:
      raise SystemError("Database schema creation failed.", { "config_dir": ConfigManager.get_config_dir() }) from e
    self._logger = LogManager.get_logger(self.__class__.__name__)

  def get_account(self, uuid: str) -> Account | None:
    try:
      account = self._database_manager.get_account_from_id(uuid)
    except DatabaseSelectException as e:
      raise DataException() from e
    return account

  def create_account(self, uuid: str, name: str,age: int, account_type: AccountType) -> Account | None:
    try:
      account = Account(
        uuid=uuid,
        name=name,
        age=age,
        account_type=account_type
      )
    except DomainValidationException as e:
      raise DataValidationException() from e
    try:
      created_account = self._database_manager.create_account(account)
    except DatabaseSelectException as e:
      raise DataException() from e
    return created_account
