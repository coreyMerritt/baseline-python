from abc import ABC

from infrastructure.logger.projectname_logger import ProjectnameLogger


class Service(ABC):
  _logger: ProjectnameLogger

  def __init__(self, logger: ProjectnameLogger):
    self._logger = logger
