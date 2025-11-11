from dataclasses import dataclass

from services.models.external_services_global_config import ExternalServicesGlobalConfig
from services.models.typicode_config import TypicodeConfig


@dataclass(frozen=True)
class ExternalServicesConfig:
  global_: ExternalServicesGlobalConfig
  typicode: TypicodeConfig
