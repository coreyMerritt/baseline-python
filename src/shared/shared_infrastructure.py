import yaml

from infrastructure.config.parser import ConfigParser
from infrastructure.database.database import Database
from infrastructure.disk.disk import Disk
from infrastructure.environment.environment import Environment
from infrastructure.logger.projectname_logger import ProjectnameLogger
from shared.enums.env_var import EnvVar

# General
environment = Environment()
DEPLOYMENT_ENV = environment.get_env_var(EnvVar.DEPLOYMENT_ENVIRONMENT)
CONFIG_DIR = f"./config/{DEPLOYMENT_ENV}"

# Handle Disk first/manually as its a dependency for other operations
DISK_CONFIG_PATH = f"{CONFIG_DIR}/disk.yml"
with open(DISK_CONFIG_PATH, "r", encoding='utf-8') as yaml_file:
  RAW_DISK_CONFIG = yaml.safe_load(yaml_file)
  DISK_CONFIG = ConfigParser().parse_disk_config(RAW_DISK_CONFIG)
  disk = Disk(DISK_CONFIG)

# Config Paths
CPU_CONFIG_PATH = f"{CONFIG_DIR}/cpu.yml"
DATABASE_CONFIG_PATH = f"{CONFIG_DIR}/database.yml"
EXTERNAL_SERVICE_CONFIG_PATH = f"{CONFIG_DIR}/external_services.yml"
LOGGER_CONFIG_PATH = f"{CONFIG_DIR}/logger.yml"
MEMORY_CONFIG_PATH = f"{CONFIG_DIR}/memory.yml"
TYPICODE_CONFIG_PATH = f"{CONFIG_DIR}/typicode.yml"

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

# Infrastructure --- These should be imported at the interface level as needed
database = Database(DATABASE_CONFIG)
logger = ProjectnameLogger(LOGGER_CONFIG)
