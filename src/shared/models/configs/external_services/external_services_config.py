from dataclasses import dataclass

from shared.models.configs.external_services.external_services_global_config import ExternalServicesGlobalConfig
from shared.models.configs.external_services.typicode_config import TypicodeConfig


@dataclass(frozen=True)
class ExternalServicesConfig:
  global_: ExternalServicesGlobalConfig
  typicode: TypicodeConfig
