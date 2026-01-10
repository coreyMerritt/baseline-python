from dataclasses import dataclass

from domain.interfaces.authenticator import AuthenticatorInterface
from infrastructure.config.parser import ConfigParser
from infrastructure.cpu.cpu import Cpu
from infrastructure.database.database import Database
from infrastructure.disk.disk import Disk
from infrastructure.environment.environment import Environment
from infrastructure.external_services.typicode_client import TypicodeClient
from infrastructure.memory.memory import Memory
from infrastructure.types.logger_interface import LoggerInterface


@dataclass
class InfrastructureCollection:
  authenticator: AuthenticatorInterface
  config_parser: ConfigParser
  cpu: Cpu
  database: Database
  disk: Disk
  environment: Environment
  logger: LoggerInterface
  memory: Memory
  typicode_client: TypicodeClient
