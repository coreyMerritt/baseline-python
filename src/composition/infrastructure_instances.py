import time
from typing import Any, Dict

import yaml

from composition.config_builders.cpu import build_final_cpu_config
from composition.config_builders.database import build_final_database_config
from composition.config_builders.disk import build_final_disk_config
from composition.config_builders.external_services import build_final_external_services_config
from composition.config_builders.logger import build_final_logger_config
from composition.config_builders.memory import build_final_memory_config
from composition.config_builders.typicode import build_final_typicode_config
from composition.enums.config_filenames import ConfigFilenames
from composition.mappers.deployment_environment_mapper import DeploymentEnvironmentMapper
from infrastructure.config.parser import ConfigParser
from infrastructure.cpu.cpu import Cpu
from infrastructure.database.account_repository import AccountRepository
from infrastructure.database.database import Database
from infrastructure.database.exceptions.database_initialization_err import DatabaseInitializationErr
from infrastructure.database.models.database_config import DatabaseConfig
from infrastructure.disk.disk import Disk
from infrastructure.environment.environment import Environment
from infrastructure.environment.models.env_var import EnvVar
from infrastructure.external_services.blog_post_repository import BlogPostRepository
from infrastructure.external_services.models.external_services_config import ExternalServicesConfig
from infrastructure.external_services.models.typicode_config import TypicodeConfig
from infrastructure.external_services.typicode_client import TypicodeClient
from infrastructure.logger.projectname_logger import ProjectnameLogger
from infrastructure.memory.memory import Memory
from shared.enums.deployment_environment import DeploymentEnvironment

def build_raw_infra() -> Dict[str, Any]:
  # Handle these first/manually as they're a dependency for proceeding operations
  _temp_environment = Environment()
  _temp_config_parser = ConfigParser()
  deployment_environment_str = _temp_environment.get_env_var(EnvVar.DEPLOYMENT_ENVIRONMENT.value)
  deployment_environment_enum = DeploymentEnvironmentMapper.str_to_enum(deployment_environment_str)
  config_dir = _build_config_dir(_temp_environment)

  # Instantiate temporary infra for this file's needs
  _temp_disk = _build_temp_disk(
    config_dir=config_dir,
    config_parser=_temp_config_parser
  )
  _temp_logger = _build_logger(
    config_dir=config_dir,
    config_parser=_temp_config_parser,
    deployment_environment_enum=deployment_environment_enum,
    disk=_temp_disk,
    temp_logger=None
  )

  # Configs for multiple builders
  external_services_config = _build_external_services_config(
    config_dir=config_dir,
    config_parser=_temp_config_parser,
    disk=_temp_disk,
    logger=_temp_logger
  )
  typicode_config = _build_typicode_config(
    config_dir=config_dir,
    config_parser=_temp_config_parser,
    disk=_temp_disk,
    logger=_temp_logger
  )
  database_config = _build_database_config(
    config_dir=config_dir,
    config_parser=_temp_config_parser,
    disk=_temp_disk,
    logger=_temp_logger
  )

  # Final Infra
  config_parser = ConfigParser()
  environment = Environment()
  logger = _build_logger(
    config_dir=config_dir,
    config_parser=config_parser,
    deployment_environment_enum=deployment_environment_enum,
    disk=_temp_disk,
    temp_logger=_temp_logger
  )
  disk = _build_disk(
    config_dir=config_dir,
    config_parser=config_parser,
    temp_disk=_temp_disk,
    logger=logger
  )
  cpu = _build_cpu(
    config_dir=config_dir,
    config_parser=config_parser,
    disk=disk,
    logger=logger
  )
  memory = _build_memory(
    config_dir=config_dir,
    config_parser=config_parser,
    disk=disk,
    logger=logger
  )
  typicode_client = _build_typicode_client(
    external_services_config=external_services_config,
    typicode_config=typicode_config
  )
  database = _build_database(
    database_config=database_config,
    logger=logger
  )
  # Final Repos
  account_repository = AccountRepository(database)
  blog_post_repository = BlogPostRepository(
    external_services_config=external_services_config,
    typicode_config=typicode_config
  )

  return {
    "vars": {
      "deployment_environment_str": deployment_environment_str,
      "deployment_environment_enum": deployment_environment_enum
    },
    "infra": {
      "config_parser": config_parser,
      "cpu": cpu,
      "database": database,
      "disk": disk,
      "environment": environment,
      "logger": logger,
      "memory": memory,
      "typicode_client": typicode_client
    },
    "repos": {
      "account": account_repository,
      "blog_post": blog_post_repository
    }
  }

def _build_config_dir(environment: Environment) -> str:
  return environment.get_env_var(EnvVar.GLOBAL_CONFIG_DIR.value)

#################### Config Builders ####################

def _build_external_services_config(
  config_dir: str,
  config_parser: ConfigParser,
  disk: Disk,
  logger: ProjectnameLogger
) -> ExternalServicesConfig:
  external_service_config_path = f"{config_dir}/{ConfigFilenames.EXTERNAL_SERVICES.value}"
  external_services_config_dict = disk.read_yaml(external_service_config_path)
  assert isinstance(external_services_config_dict, dict)
  return build_final_external_services_config(
    config_parser=config_parser,
    logger=logger,
    external_services_config_dict=external_services_config_dict
  )

def _build_typicode_config(
  config_dir: str,
  config_parser: ConfigParser,
  disk: Disk,
  logger: ProjectnameLogger
) -> TypicodeConfig:
  typicode_config_path = f"{config_dir}/{ConfigFilenames.TYPICODE.value}"
  typicode_config_dict = disk.read_yaml(typicode_config_path)
  assert isinstance(typicode_config_dict, dict)
  return build_final_typicode_config(
    config_parser=config_parser,
    logger=logger,
    typicode_config_dict=typicode_config_dict
  )

def _build_database_config(
  config_dir: str,
  config_parser: ConfigParser,
  disk: Disk,
  logger: ProjectnameLogger
) -> DatabaseConfig:
  database_config_path = f"{config_dir}/{ConfigFilenames.DATABASE.value}"
  database_config_dict = disk.read_yaml(database_config_path)
  assert isinstance(database_config_dict, dict)
  return build_final_database_config(
    config_parser=config_parser,
    logger=logger,
    database_config_dict=database_config_dict
  )

#################### Infra Builders ####################

def _build_temp_disk(config_dir: str, config_parser: ConfigParser) -> Disk:
  disk_config_path = f"{config_dir}/{ConfigFilenames.DISK.value}"
  with open(disk_config_path, "r", encoding='utf-8') as yaml_file:
    raw_disk_config = yaml.safe_load(yaml_file)
    disk_config = config_parser.parse_disk_config(raw_disk_config)
    return Disk(disk_config)

def _build_logger(
  config_dir: str,
  config_parser: ConfigParser,
  deployment_environment_enum: DeploymentEnvironment,
  disk: Disk,
  temp_logger: ProjectnameLogger | None
) -> ProjectnameLogger:
  logger_config_path = f"{config_dir}/{ConfigFilenames.LOGGER.value}"
  logger_config_dict = disk.read_yaml(logger_config_path)
  assert isinstance(logger_config_dict, dict)
  logger_config = build_final_logger_config(
    config_parser=config_parser,
    logger=temp_logger,
    logger_config_dict=logger_config_dict
  )
  return ProjectnameLogger(deployment_environment_enum, logger_config)

def _build_cpu(
  config_dir: str,
  config_parser: ConfigParser,
  disk: Disk,
  logger:ProjectnameLogger
) -> Cpu:
  cpu_config_path = f"{config_dir}/{ConfigFilenames.CPU.value}"
  cpu_config_dict = disk.read_yaml(cpu_config_path)
  assert isinstance(cpu_config_dict, dict)
  cpu_config = build_final_cpu_config(
    config_parser=config_parser,
    logger=logger,
    cpu_config_dict=cpu_config_dict
  )
  return Cpu(cpu_config)

def _build_disk(
  config_dir: str,
  config_parser: ConfigParser,
  temp_disk: Disk,
  logger: ProjectnameLogger
) -> Disk:
  disk_config_path = f"{config_dir}/{ConfigFilenames.DISK.value}"
  disk_config_dict = temp_disk.read_yaml(disk_config_path)
  assert isinstance(disk_config_dict, dict)
  disk_config = build_final_disk_config(
    config_parser=config_parser,
    logger=logger,
    disk_config_dict=disk_config_dict,
  )
  return Disk(disk_config)

def _build_memory(
  config_dir: str,
  config_parser: ConfigParser,
  disk: Disk,
  logger: ProjectnameLogger
) -> Memory:
  memory_config_path = f"{config_dir}/{ConfigFilenames.MEMORY.value}"
  memory_config_dict = disk.read_yaml(memory_config_path)
  assert isinstance(memory_config_dict, dict)
  memory_config = build_final_memory_config(
    config_parser=config_parser,
    logger=logger,
    memory_config_dict=memory_config_dict
  )
  return Memory(memory_config)

def _build_typicode_client(
  external_services_config: ExternalServicesConfig,
  typicode_config: TypicodeConfig
) -> TypicodeClient:
  return TypicodeClient(external_services_config, typicode_config)


def _build_database(
  database_config: DatabaseConfig,
  logger: ProjectnameLogger
) -> Database:
  TIMEOUT = 3600.0
  RETRY_TIME = 5.0
  last_err = Exception()
  start_time = time.time()
  while time.time() - start_time < TIMEOUT:
    try:
      return Database(database_config)
    except DatabaseInitializationErr as e:
      last_err = e
      logger.error("Failed to connect to database. Trying again...", error=e)
      time.sleep(RETRY_TIME)
  if time.time() - start_time >= TIMEOUT:
    logger.critical("Timed our waiting for database initialization", error=last_err)
  raise TimeoutError("Timed out trying to connect to database.")
