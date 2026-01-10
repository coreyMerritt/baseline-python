from typing import Any, Dict

from composition.config_builders._helpers import get_final_config_var
from infrastructure.config.parser import ConfigParser
from infrastructure.auth.models.token_issuer_config import TokenIssuerConfig
from infrastructure.environment.models.env_var import EnvVar
from infrastructure.logger.foo_project_name_logger import FooProjectNameLogger


def build_final_token_issuer_config(
  config_parser: ConfigParser,
  logger: FooProjectNameLogger,
  token_issuer_config_dict: Dict[str, Any]
) -> TokenIssuerConfig:
  _ = config_parser.parse_token_issuer_config(token_issuer_config_dict)
  token_issuer_config_dict["time_to_live"] = get_final_config_var(
    logger=logger,
    config_var=token_issuer_config_dict["time_to_live"],
    env_var=EnvVar.MEMORY_MAXIMUM_HEALTHY_USAGE_PERCENTAGE
  )
  return config_parser.parse_token_issuer_config(token_issuer_config_dict)
