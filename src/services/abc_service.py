from abc import ABC

from infrastructure.config.parser import ConfigParser
from infrastructure.disk.disk import Disk
from infrastructure.disk.exceptions.disk_read_err import DiskReadErr
from infrastructure.environment.environment import Environment
from infrastructure.logger.projectname_logger import ProjectnameLogger
from services.enums.env_var import EnvVar
from services.exceptions.config_load_exception import ConfigLoadErr
from shared.models.configs.logger_config import LoggerConfig


class Service(ABC):
  _logger: ProjectnameLogger

  def __init__(self):
    logger_config = self._get_logger_config()
    self._logger = ProjectnameLogger(logger_config)

  def _get_logger_config(self) -> LoggerConfig:
    environment = Environment()
    config_dir = environment.get_env_var(EnvVar.DEPLOYMENT_ENVIRONMENT)
    logger_config_path = f"./config/{config_dir}/logger.yml"
    try:
      raw_logger_config = Disk().read_yaml(logger_config_path)
    except DiskReadErr as e:
      raise ConfigLoadErr(logger_config_path) from e
    return ConfigParser().parse_logger_config(raw_logger_config)
