from dataclasses import dataclass

from infrastructure.config.models.external_services_global_config import ExternalServicesGlobalConfig
from infrastructure.config.models.typicode_config import TypicodeConfig


@dataclass(frozen=True)
class ExternalServicesConfig:
  global_: ExternalServicesGlobalConfig
  typicode: TypicodeConfig
