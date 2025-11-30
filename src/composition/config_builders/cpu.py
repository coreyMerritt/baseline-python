from typing import Any, Dict

from composition.config_builders._helpers import get_final_config_var
from infrastructure.config.parser import ConfigParser
from infrastructure.cpu.models.cpu_config import CpuConfig
from infrastructure.environment.models.env_var import EnvVar
from infrastructure.logger.projectname_logger import ProjectnameLogger


def build_final_cpu_config(
  config_parser: ConfigParser,
  logger: ProjectnameLogger,
  cpu_config_dict: Dict[str, Any]
) -> CpuConfig:
  _ = config_parser.parse_cpu_config(cpu_config_dict)
  assert cpu_config_dict["check_interval_seconds"], "check_interval_seconds not in cpu configuration file"
  cpu_config_dict["check_interval_seconds"] = get_final_config_var(
    logger=logger,
    config_var=cpu_config_dict["check_interval_seconds"],
    env_var=EnvVar.CPU_CHECK_INTERVAL_SECONDS
  )
  assert cpu_config_dict["maximum_healthy_usage_percentage"], {
    "maximum_healthy_usage_percentage not in cpu configuration file"
  }
  cpu_config_dict["maximum_healthy_usage_percentage"] = get_final_config_var(
    logger=logger,
    config_var=cpu_config_dict["maximum_healthy_usage_percentage"],
    env_var=EnvVar.CPU_MAXIMUM_HEALTHY_USAGE_PERCENTAGE
  )
  return config_parser.parse_cpu_config(cpu_config_dict)
