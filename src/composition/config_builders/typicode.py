from typing import Any, Dict

from composition.config_builders._helpers import get_final_config_var
from infrastructure.config.parser import ConfigParser
from infrastructure.environment.models.env_var import EnvVar
from infrastructure.external_services.models.typicode_config import TypicodeConfig
from infrastructure.logger.projectname_logger import ProjectnameLogger


def build_final_typicode_config(
  config_parser: ConfigParser,
  logger: ProjectnameLogger,
  typicode_config_dict: Dict[str, Any]
) -> TypicodeConfig:
  _ = config_parser.parse_typicode_config(typicode_config_dict)
  assert typicode_config_dict["placeholder"], "placeholder not in typicode configuration file"
  typicode_config_dict["placeholder"] = get_final_config_var(
    logger=logger,
    config_var=typicode_config_dict["placeholder"],
    env_var=EnvVar.TYPICODE_PLACEHOLDER
  )
  return config_parser.parse_typicode_config(typicode_config_dict)
