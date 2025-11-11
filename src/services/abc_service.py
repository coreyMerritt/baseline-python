from abc import ABC

from infrastructure.logging.projectname_logger import Logger, ProjectnameLogger


class Service(ABC):
  _logger: Logger

  def __init__(self):
    self._logger = ProjectnameLogger.get_logger(self.__class__.__name__)
