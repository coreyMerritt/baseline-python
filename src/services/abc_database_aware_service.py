from services.abc_service import Service
from services.database_manager import DatabaseManager


class DatabaseAwareService(Service):
  _database_manager: DatabaseManager

  def __init__(self, database_manager: DatabaseManager):
    self._database_manager = database_manager
    super().__init__()
