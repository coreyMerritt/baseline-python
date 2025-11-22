from dataclasses import dataclass

from infrastructure.config.parser import ConfigParser
from infrastructure.cpu.cpu import Cpu
from infrastructure.database.database import Database
from infrastructure.disk.disk import Disk
from infrastructure.environment.environment import Environment
from infrastructure.external_services.typicode_client import TypicodeClient
from infrastructure.logger.projectname_logger import ProjectnameLogger
from infrastructure.memory.memory import Memory


@dataclass
class Infra:
  config_parser: ConfigParser
  cpu: Cpu
  database: Database
  disk: Disk
  environment: Environment
  logger: ProjectnameLogger
  memory: Memory
  typicode_client: TypicodeClient
