from infrastructure.database.database import Database
from infrastructure.database.exceptions.database_initialization_err import DatabaseInitializationErr
from services.abc_service import Service
from services.exceptions.service_initialization_err import ServiceInitializationErr


class DatabaseAwareService(Service):
  _database: Database

  def __init__(self, database: Database):
    try:
      self._database = database
    except DatabaseInitializationErr as e:
      raise ServiceInitializationErr() from e
    super().__init__()
