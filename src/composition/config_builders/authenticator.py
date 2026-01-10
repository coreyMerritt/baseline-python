import os

from infrastructure.config.parser import ConfigParser
from infrastructure.auth.models.authenticator_config import AuthenticatorConfig
from infrastructure.environment.models.env_var import EnvVar


def build_final_authenticator_config(
  config_parser: ConfigParser
) -> AuthenticatorConfig:
  authenticator_config_dict = {}
  authenticator_config_dict["secret"] = os.getenv(EnvVar.AUTHENTICATOR_SECRET.value)
  return config_parser.parse_authenticator_config(authenticator_config_dict)
