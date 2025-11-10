from abc import ABC
from logging import Logger

from infrastructure.config.config_manager import ConfigManager
from infrastructure.database.database_manager import DatabaseManager
from infrastructure.database.exceptions.database_schema_creation_exception import DatabaseSchemaCreationException
from infrastructure.logging.log_manager import LogManager
from services.exceptions.service_initialization_exception import ServiceInitializationException


class Service(ABC):
  _database_manager: DatabaseManager
  _logger: Logger

  def __init__(self):
    database_config = ConfigManager.get_database_config()
    try:
      self._database_manager = DatabaseManager(database_config)
    except DatabaseSchemaCreationException as e:
      raise ServiceInitializationException(
        "Database schema creation failed.",
        {"config_dir": ConfigManager.get_config_dir()}
      ) from e
    self._logger = LogManager.get_logger(self.__class__.__name__)
