from infrastructure.logger.projectname_logger import ProjectnameLogger


class Service():
  _logger: ProjectnameLogger

  def __init__(self, logger: ProjectnameLogger):
    self._logger = logger
    assert not isinstance(self, Service), "Service is a base class and should not be instantiated"
