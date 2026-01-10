import os

from infrastructure.config.parser import ConfigParser
from infrastructure.auth.models.token_hasher_config import TokenHasherConfig
from infrastructure.environment.models.env_var import EnvVar


def build_final_token_hasher_config(
  config_parser: ConfigParser
) -> TokenHasherConfig:
  token_hasher_config_dict = {}
  token_hasher_config_dict["secret"] = os.getenv(EnvVar.TOKEN_HASHER_SECRET.value)
  return config_parser.parse_token_hasher_config(token_hasher_config_dict)
