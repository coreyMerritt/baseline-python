from abc import ABC

from infrastructure.config.parser import ConfigParser
from infrastructure.disk.disk import Disk
from infrastructure.environment.environment import Environment
from infrastructure.logger.projectname_logger import ProjectnameLogger
from services.enums.env_var import EnvVar
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
    raw_logger_config = Disk().read_yaml(logger_config_path)
    return ConfigParser().parse_logger_config(raw_logger_config)
