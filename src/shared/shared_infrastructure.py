from infrastructure.config.parser import ConfigParser
from infrastructure.database.database import Database
from infrastructure.disk.disk import Disk
from infrastructure.environment.environment import Environment
from infrastructure.logger.projectname_logger import ProjectnameLogger
from services.enums.env_var import EnvVar

# General
environment = Environment()
DEPLOYMENT_ENV = environment.get_env_var(EnvVar.DEPLOYMENT_ENVIRONMENT)
CONFIG_DIR = f"./config/{DEPLOYMENT_ENV}"

# Config Paths
DATABASE_CONFIG_PATH = f"{CONFIG_DIR}/database.yml"
LOGGER_CONFIG_PATH = f"{CONFIG_DIR}/logger.yml"
EXTERNAL_SERVICE_CONFIG_PATH = f"{CONFIG_DIR}/external_services.yml"
HEALTH_CHECK_CONFIG_PATH = f"{CONFIG_DIR}/health_check.yml"

# Raw Configs
RAW_DATABASE_CONFIG = Disk().read_yaml(DATABASE_CONFIG_PATH)
RAW_LOGGER_CONFIG = Disk().read_yaml(LOGGER_CONFIG_PATH)
RAW_EXTERNAL_SERVICE_CONFIG = Disk().read_yaml(EXTERNAL_SERVICE_CONFIG_PATH)
RAW_HEALTH_CHECK_CONFIG = Disk().read_yaml(HEALTH_CHECK_CONFIG_PATH)

# Configs --- These should be imported at the interface level as needed
DATABASE_CONFIG = ConfigParser().parse_database_config(RAW_DATABASE_CONFIG)
LOGGER_CONFIG = ConfigParser().parse_logger_config(RAW_LOGGER_CONFIG)
EXTERNAL_SERVICES_CONFIG = ConfigParser().parse_external_services_config(RAW_EXTERNAL_SERVICE_CONFIG)
HEALTH_CHECK_CONFIG = ConfigParser().parse_health_check_config(RAW_HEALTH_CHECK_CONFIG)

# Infrastructure --- These should be imported at the interface level as needed
database = Database(DATABASE_CONFIG)
logger = ProjectnameLogger(LOGGER_CONFIG)
