import yaml

from composition.enums.config_filenames import ConfigFilenames
from infrastructure.config.parser import ConfigParser
from infrastructure.cpu.cpu import Cpu
from infrastructure.database.account_repository import AccountRepository
from infrastructure.database.database import Database
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
_GLOBAL_CONFIG_DIR = _environment.get_env_var(EnvVar.GLOBAL_CONFIG_DIR.value)
_CONFIG_DIR = f"{_GLOBAL_CONFIG_DIR}/{_DEPLOYMENT_ENVIRONMENT_STR}"
_config_parser = ConfigParser()
_DISK_CONFIG_PATH = f"{_CONFIG_DIR}/{ConfigFilenames.DISK.value}"
with open(_DISK_CONFIG_PATH, "r", encoding='utf-8') as yaml_file:
  _RAW_DISK_CONFIG = yaml.safe_load(yaml_file)
  _DISK_CONFIG = _config_parser.parse_disk_config(_RAW_DISK_CONFIG)
  _disk = Disk(_DISK_CONFIG)

# Config Paths
_CPU_CONFIG_PATH = f"{_CONFIG_DIR}/{ConfigFilenames.CPU.value}"
_DATABASE_CONFIG_PATH = f"{_CONFIG_DIR}/{ConfigFilenames.DATABASE.value}"
_EXTERNAL_SERVICE_CONFIG_PATH = f"{_CONFIG_DIR}/{ConfigFilenames.EXTERNAL_SERVICES.value}"
_LOGGER_CONFIG_PATH = f"{_CONFIG_DIR}/{ConfigFilenames.LOGGER.value}"
_MEMORY_CONFIG_PATH = f"{_CONFIG_DIR}/{ConfigFilenames.MEMORY.value}"
_TYPICODE_CONFIG_PATH = f"{_CONFIG_DIR}/{ConfigFilenames.TYPICODE.value}"

# Raw Configs
_RAW_CPU_CONFIG = _disk.read_yaml(_CPU_CONFIG_PATH)
_RAW_DATABASE_CONFIG = _disk.read_yaml(_DATABASE_CONFIG_PATH)
_RAW_EXTERNAL_SERVICES_CONFIG = _disk.read_yaml(_EXTERNAL_SERVICE_CONFIG_PATH)
_RAW_LOGGER_CONFIG = _disk.read_yaml(_LOGGER_CONFIG_PATH)
_RAW_MEMORY_CONFIG = _disk.read_yaml(_MEMORY_CONFIG_PATH)
_RAW_TYPICODE_CONFIG = _disk.read_yaml(_TYPICODE_CONFIG_PATH)

# Configs
_CPU_CONFIG = _config_parser.parse_cpu_config(_RAW_CPU_CONFIG)
_DATABASE_CONFIG = _config_parser.parse_database_config(_RAW_DATABASE_CONFIG)
_EXTERNAL_SERVICES_CONFIG = _config_parser.parse_external_services_config(_RAW_EXTERNAL_SERVICES_CONFIG)
_LOGGER_CONFIG = _config_parser.parse_logger_config(_RAW_LOGGER_CONFIG)
_MEMORY_CONFIG = _config_parser.parse_memory_config(_RAW_MEMORY_CONFIG)
_TYPICODE_CONFIG = _config_parser.parse_typicode_config(_RAW_TYPICODE_CONFIG)

# Infrastructure --- These should be imported at the composition-level as needed
DEPLOYMENT_ENVIRONMENT_STR = _DEPLOYMENT_ENVIRONMENT_STR
config_parser = _config_parser
cpu = Cpu(_CPU_CONFIG)
database = Database(_DATABASE_CONFIG)
disk = _disk
environment = _environment
logger = ProjectnameLogger(_LOGGER_CONFIG)
memory = Memory(_MEMORY_CONFIG)
typicode_client = TypicodeClient(_EXTERNAL_SERVICES_CONFIG, _TYPICODE_CONFIG)
account_repository = AccountRepository(database)
blog_post_repository = BlogPostRepository(_EXTERNAL_SERVICES_CONFIG, _TYPICODE_CONFIG)
