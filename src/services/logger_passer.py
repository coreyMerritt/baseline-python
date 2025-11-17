from infrastructure.config.parser import ConfigParser
from infrastructure.disk.disk import Disk
from infrastructure.disk.exceptions.disk_read_err import DiskReadErr
from infrastructure.environment.environment import Environment
from infrastructure.logger.projectname_logger import ProjectnameLogger
from services.abc_service import Service
from services.enums.env_var import EnvVar
from services.exceptions.config_load_exception import ConfigLoadErr
from shared.models.configs.logger_config import LoggerConfig


# This service exists solely to get loggers to the interface layer as needed. Not sure I love thiss
class LoggerPasser(Service):
  def get_logger(self) -> ProjectnameLogger:
    logger_config = self._get_logger_config()
    logger = ProjectnameLogger(logger_config)
    return logger

  def _get_logger_config(self) -> LoggerConfig:
    environment = Environment()
    config_dir = environment.get_env_var(EnvVar.DEPLOYMENT_ENVIRONMENT)
    logger_config_path = f"{config_dir}/logger.yml"
    try:
      raw_logger_config = Disk().read_yaml(logger_config_path)
    except DiskReadErr as e:
      raise ConfigLoadErr() from e
    return ConfigParser().parse_logger_config(raw_logger_config)
