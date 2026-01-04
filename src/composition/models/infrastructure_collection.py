from dataclasses import dataclass

from infrastructure.config.parser import ConfigParser
from infrastructure.cpu.cpu import Cpu
from infrastructure.database.database import Database
from infrastructure.disk.disk import Disk
from infrastructure.environment.environment import Environment
from infrastructure.external_services.typicode_client import TypicodeClient
from infrastructure.logger.foo_project_name_logger import FooProjectNameLogger
from infrastructure.memory.memory import Memory


@dataclass
class InfrastructureCollection:
  config_parser: ConfigParser
  cpu: Cpu
  database: Database
  disk: Disk
  environment: Environment
  logger: FooProjectNameLogger
  memory: Memory
  typicode_client: TypicodeClient
