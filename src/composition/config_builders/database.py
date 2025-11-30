from typing import Any, Dict

from composition.config_builders._helpers import get_final_config_var
from infrastructure.config.parser import ConfigParser
from infrastructure.database.models.database_config import DatabaseConfig
from infrastructure.environment.models.env_var import EnvVar
from infrastructure.logger.projectname_logger import ProjectnameLogger


def build_final_database_config(
  config_parser: ConfigParser,
  logger: ProjectnameLogger,
  database_config_dict: Dict[str, Any]
) -> DatabaseConfig:
  _ = config_parser.parse_database_config(database_config_dict)
  assert database_config_dict["engine"], "engine not in database configuration file"
  database_config_dict["engine"] = get_final_config_var(
    logger=logger,
    config_var=database_config_dict["engine"],
    env_var=EnvVar.DATABASE_ENGINE
  )
  assert database_config_dict["host"], "host not in database configuration file"
  database_config_dict["host"] = get_final_config_var(
    logger=logger,
    config_var=database_config_dict["host"],
    env_var=EnvVar.DATABASE_HOST
  )
  assert database_config_dict["name"], "name not in database configuration file"
  database_config_dict["name"] = get_final_config_var(
    logger=logger,
    config_var=database_config_dict["name"],
    env_var=EnvVar.DATABASE_NAME
  )
  assert database_config_dict["password"], "password not in database configuration file"
  database_config_dict["password"] = get_final_config_var(
    logger=logger,
    config_var=database_config_dict["password"],
    env_var=EnvVar.DATABASE_PASSWORD
  )
  assert database_config_dict["port"], "port not in database configuration file"
  database_config_dict["port"] = get_final_config_var(
    logger=logger,
    config_var=database_config_dict["port"],
    env_var=EnvVar.DATABASE_PORT
  )
  assert database_config_dict["username"], "username not in database configuration file"
  database_config_dict["username"] = get_final_config_var(
    logger=logger,
    config_var=database_config_dict["username"],
    env_var=EnvVar.DATABASE_USERNAME
  )
  return config_parser.parse_database_config(database_config_dict)
