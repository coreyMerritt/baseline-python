from infrastructure.database.database import Database
from infrastructure.database.exceptions.database_initialization_err import DatabaseInitializationErr
from infrastructure.logger.projectname_logger import ProjectnameLogger
from services.base_service import Service
from services.exceptions.service_initialization_err import ServiceInitializationErr


class DatabaseAwareService(Service):
  _database: Database

  def __init__(self, logger: ProjectnameLogger, database: Database):
    try:
      self._database = database
    except DatabaseInitializationErr as e:
      raise ServiceInitializationErr() from e
    super().__init__(logger)
