from abc import ABC
from logging import Logger

from infrastructure.logging.log_manager import LogManager


class Service(ABC):
  _logger: Logger

  def __init__(self):
    self._logger = LogManager.get_logger(self.__class__.__name__)
