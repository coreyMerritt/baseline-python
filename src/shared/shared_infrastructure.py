import yaml

from infrastructure.config.parser import ConfigParser
from infrastructure.database.account_repository import AccountRepository
from infrastructure.database.database import Database
from infrastructure.disk.disk import Disk
from infrastructure.environment.environment import Environment
from infrastructure.external_services.blog_post_repository import BlogPostRepository
from infrastructure.logger.projectname_logger import ProjectnameLogger
from shared.enums.config_filenames import ConfigFilenames
from shared.enums.env_var import EnvVar

# General
__environment = Environment()
__DEPLOYMENT_ENV = __environment.get_env_var(EnvVar.DEPLOYMENT_ENVIRONMENT)
__CONFIG_DIR = f"./config/{__DEPLOYMENT_ENV}"

# Handle Disk first/manually as its a dependency for other operations
DISK_CONFIG_PATH = f"{__CONFIG_DIR}/{ConfigFilenames.DISK.value}"
with open(DISK_CONFIG_PATH, "r", encoding='utf-8') as yaml_file:
  RAW_DISK_CONFIG = yaml.safe_load(yaml_file)
  DISK_CONFIG = ConfigParser().parse_disk_config(RAW_DISK_CONFIG)
  disk = Disk(DISK_CONFIG)

# Config Paths
CPU_CONFIG_PATH = f"{__CONFIG_DIR}/{ConfigFilenames.CPU.value}"
DATABASE_CONFIG_PATH = f"{__CONFIG_DIR}/{ConfigFilenames.DATABASE.value}"
EXTERNAL_SERVICE_CONFIG_PATH = f"{__CONFIG_DIR}/{ConfigFilenames.EXTERNAL_SERVICES.value}"
LOGGER_CONFIG_PATH = f"{__CONFIG_DIR}/{ConfigFilenames.LOGGER.value}"
MEMORY_CONFIG_PATH = f"{__CONFIG_DIR}/{ConfigFilenames.MEMORY.value}"
TYPICODE_CONFIG_PATH = f"{__CONFIG_DIR}/{ConfigFilenames.TYPICODE.value}"

# Raw Configs
RAW_CPU_CONFIG = disk.read_yaml(CPU_CONFIG_PATH)
RAW_DATABASE_CONFIG = disk.read_yaml(DATABASE_CONFIG_PATH)
RAW_EXTERNAL_SERVICE_CONFIG = disk.read_yaml(EXTERNAL_SERVICE_CONFIG_PATH)
RAW_LOGGER_CONFIG = disk.read_yaml(LOGGER_CONFIG_PATH)
RAW_MEMORY_CONFIG = disk.read_yaml(MEMORY_CONFIG_PATH)
RAW_TYPICODE_CONFIG = disk.read_yaml(TYPICODE_CONFIG_PATH)

# Configs --- These should be imported at the interface level as needed
CPU_CONFIG = ConfigParser().parse_cpu_config(RAW_CPU_CONFIG)
DATABASE_CONFIG = ConfigParser().parse_database_config(RAW_DATABASE_CONFIG)
EXTERNAL_SERVICES_CONFIG = ConfigParser().parse_external_services_config(RAW_EXTERNAL_SERVICE_CONFIG)
LOGGER_CONFIG = ConfigParser().parse_logger_config(RAW_LOGGER_CONFIG)
MEMORY_CONFIG = ConfigParser().parse_memory_config(RAW_MEMORY_CONFIG)
TYPICODE_CONFIG = ConfigParser().parse_typicode_config(RAW_TYPICODE_CONFIG)

# BaseInfrastructure --- These should be imported at the interface level as needed
database = Database(DATABASE_CONFIG)
logger = ProjectnameLogger(LOGGER_CONFIG)
account_repository = AccountRepository(database)
blog_post_repository = BlogPostRepository(EXTERNAL_SERVICES_CONFIG, TYPICODE_CONFIG)
