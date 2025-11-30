import time
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
from infrastructure.disk.disk import Disk
from infrastructure.environment.environment import Environment
from infrastructure.environment.models.env_var import EnvVar
from infrastructure.external_services.blog_post_repository import BlogPostRepository
from infrastructure.external_services.typicode_client import TypicodeClient
from infrastructure.logger.projectname_logger import ProjectnameLogger
from infrastructure.memory.memory import Memory

# Handle these first/manually as they're a dependency for proceeding operations
_environment = Environment()
_environment.load_env()
_DEPLOYMENT_ENVIRONMENT_STR = _environment.get_env_var(EnvVar.DEPLOYMENT_ENVIRONMENT.value)
_DEPLOYMENT_ENVIRONMENT_ENUM = DeploymentEnvironmentMapper.str_to_enum(_DEPLOYMENT_ENVIRONMENT_STR)
_GLOBAL_CONFIG_DIR = _environment.get_env_var(EnvVar.GLOBAL_CONFIG_DIR.value)
_CONFIG_DIR = f"{_GLOBAL_CONFIG_DIR}/{_DEPLOYMENT_ENVIRONMENT_STR}"
_config_parser = ConfigParser()
_DISK_CONFIG_PATH = f"{_CONFIG_DIR}/{ConfigFilenames.DISK.value}"
with open(_DISK_CONFIG_PATH, "r", encoding='utf-8') as yaml_file:
  _RAW_DISK_CONFIG = yaml.safe_load(yaml_file)
  _disk_config = _config_parser.parse_disk_config(_RAW_DISK_CONFIG)
  _disk = Disk(_disk_config)

# Config Paths
_CPU_CONFIG_PATH = f"{_CONFIG_DIR}/{ConfigFilenames.CPU.value}"
_DATABASE_CONFIG_PATH = f"{_CONFIG_DIR}/{ConfigFilenames.DATABASE.value}"
_EXTERNAL_SERVICE_CONFIG_PATH = f"{_CONFIG_DIR}/{ConfigFilenames.EXTERNAL_SERVICES.value}"
_LOGGER_CONFIG_PATH = f"{_CONFIG_DIR}/{ConfigFilenames.LOGGER.value}"
_MEMORY_CONFIG_PATH = f"{_CONFIG_DIR}/{ConfigFilenames.MEMORY.value}"
_TYPICODE_CONFIG_PATH = f"{_CONFIG_DIR}/{ConfigFilenames.TYPICODE.value}"

# Config Dicts
_CPU_CONFIG_DICT = _disk.read_yaml(_CPU_CONFIG_PATH)
_DATABASE_CONFIG_DICT = _disk.read_yaml(_DATABASE_CONFIG_PATH)
_DISK_CONFIG_DICT = _disk.read_yaml(_DISK_CONFIG_PATH)
_EXTERNAL_SERVICES_CONFIG_DICT = _disk.read_yaml(_EXTERNAL_SERVICE_CONFIG_PATH)
_LOGGER_CONFIG_DICT = _disk.read_yaml(_LOGGER_CONFIG_PATH)
_MEMORY_CONFIG_DICT = _disk.read_yaml(_MEMORY_CONFIG_PATH)
_TYPICODE_CONFIG_DICT = _disk.read_yaml(_TYPICODE_CONFIG_PATH)
assert isinstance(_CPU_CONFIG_DICT, dict)
assert isinstance(_DATABASE_CONFIG_DICT, dict)
assert isinstance(_DISK_CONFIG_DICT, dict)
assert isinstance(_EXTERNAL_SERVICES_CONFIG_DICT, dict)
assert isinstance(_LOGGER_CONFIG_DICT, dict)
assert isinstance(_MEMORY_CONFIG_DICT, dict)
assert isinstance(_TYPICODE_CONFIG_DICT, dict)

# Instantiate a temporary logger for this file's needs
_temp_logger_config = _config_parser.parse_logger_config(_LOGGER_CONFIG_DICT)
_temp_logger = ProjectnameLogger(_DEPLOYMENT_ENVIRONMENT_ENUM, _temp_logger_config)

# Final configs
_CPU_CONFIG = build_final_cpu_config(
  config_parser=_config_parser,
  logger=_temp_logger,
  cpu_config_dict=_CPU_CONFIG_DICT
)
_DATABASE_CONFIG = build_final_database_config(
  config_parser=_config_parser,
  logger=_temp_logger,
  database_config_dict=_DATABASE_CONFIG_DICT
)
_DISK_CONFIG = build_final_disk_config(
  config_parser=_config_parser,
  logger=_temp_logger,
  disk_config_dict=_DISK_CONFIG_DICT
)
_EXTERNAL_SERVICES_CONFIG = build_final_external_services_config(
  config_parser=_config_parser,
  logger=_temp_logger,
  external_services_config_dict=_EXTERNAL_SERVICES_CONFIG_DICT
)
_LOGGER_CONFIG = build_final_logger_config(
  config_parser=_config_parser,
  logger=_temp_logger,
  logger_config_dict=_LOGGER_CONFIG_DICT
)
_MEMORY_CONFIG = build_final_memory_config(
  config_parser=_config_parser,
  logger=_temp_logger,
  memory_config_dict=_MEMORY_CONFIG_DICT
)
_TYPICODE_CONFIG = build_final_typicode_config(
  config_parser=_config_parser,
  logger=_temp_logger,
  typicode_config_dict=_TYPICODE_CONFIG_DICT
)

# IMPORT ME - Infra
DEPLOYMENT_ENVIRONMENT_STR = _DEPLOYMENT_ENVIRONMENT_STR
DEPLOYMENT_ENVIRONMENT_ENUM = _DEPLOYMENT_ENVIRONMENT_ENUM
config_parser = _config_parser
cpu = Cpu(_CPU_CONFIG)
disk = Disk(_DISK_CONFIG)
environment = _environment
logger = ProjectnameLogger(_DEPLOYMENT_ENVIRONMENT_ENUM, _LOGGER_CONFIG)
memory = Memory(_MEMORY_CONFIG)
typicode_client = TypicodeClient(_EXTERNAL_SERVICES_CONFIG, _TYPICODE_CONFIG)

# IMPORT ME - Database
TIMEOUT = 3600.0
RETRY_TIME = 5.0
last_err = Exception()
start_time = time.time()
while time.time() - start_time < TIMEOUT:
  try:
    database = Database(_DATABASE_CONFIG)
    break
  except DatabaseInitializationErr as e:
    last_err = e
    logger.error("Failed to connect to database. Trying again...", error=e)
    logger.error(f"Engine: {_DATABASE_CONFIG.engine}", error=None)
    logger.error(f"Host: {_DATABASE_CONFIG.host}", error=None)
    logger.error(f"Name: {_DATABASE_CONFIG.name}", error=None)
    logger.error(f"Password: {_DATABASE_CONFIG.password}", error=None)
    logger.error(f"Port: {_DATABASE_CONFIG.port}", error=None)
    logger.error(f"Username: {_DATABASE_CONFIG.username}", error=None)
    time.sleep(RETRY_TIME)
if time.time() - start_time >= TIMEOUT:
  logger.critical("Timed our waiting for database initialization", error=last_err)

# IMPORT ME - Repositories
account_repository = AccountRepository(database)
blog_post_repository = BlogPostRepository(_EXTERNAL_SERVICES_CONFIG, _TYPICODE_CONFIG)
