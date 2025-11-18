from dataclasses import dataclass

from shared.models.configs.base_config import Config


@dataclass(frozen=True)
class ExternalServicesConfig(Config):
  request_timeout: float
