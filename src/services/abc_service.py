from abc import ABC
from logging import Logger

from infrastructure.logger.projectname_logger import ProjectnameLogger


class Service(ABC):
  _logger: Logger

  def __init__(self):
    self._logger = ProjectnameLogger.get_logger(self.__class__.__name__)
