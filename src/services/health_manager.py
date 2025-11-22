import json
from dataclasses import asdict

from infrastructure.config.parser import ConfigParser
from infrastructure.cpu.cpu import Cpu
from infrastructure.cpu.models.cpu_config import CpuConfig
from infrastructure.database.database import Database
from infrastructure.disk.disk import Disk
from infrastructure.disk.models.disk_config import DiskConfig
from infrastructure.environment.environment import Environment
from infrastructure.external_services.models.external_services_config import ExternalServicesConfig
from infrastructure.external_services.models.typicode_config import TypicodeConfig
from infrastructure.external_services.typicode_client import TypicodeClient
from infrastructure.memory.memory import Memory
from infrastructure.memory.models.memory_config import MemoryConfig
from services.base_service import BaseService
from shared.models.health_reports.full_health_report import FullHealthReport


class HealthManager(BaseService):
  def get_full_health_report(
    self,
    database: Database,
    cpu_config: CpuConfig,
    disk_config: DiskConfig,
    external_services_config: ExternalServicesConfig,
    memory_config: MemoryConfig,
    typicode_config: TypicodeConfig
  ) -> FullHealthReport:
    config_parser_health_report = ConfigParser().get_health_report()
    cpu_health_report = Cpu(cpu_config).get_health_report()
    database_health_report = database.get_health_report()
    disk_health_report = Disk(disk_config).get_health_report()
    environment_health_report = Environment().get_health_report()
    logger_health_report = self._logger.get_health_report()
    memory_health_report = Memory(memory_config).get_health_report()
    typicode_health_report = TypicodeClient(external_services_config, typicode_config).get_health_report()
    full_health_report = FullHealthReport(
      config_parser_health_report=config_parser_health_report,
      cpu_health_report=cpu_health_report,
      database_health_report=database_health_report,
      disk_health_report=disk_health_report,
      environment_health_report=environment_health_report,
      logger_health_report=logger_health_report,
      memory_health_report=memory_health_report,
      typicode_health_report=typicode_health_report
    )
    self._logger.debug("System Health:\n%s", json.dumps(asdict(full_health_report), indent=2))
    return full_health_report
