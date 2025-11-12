from dataclasses import dataclass


@dataclass(frozen=True)
class ExternalServicesGlobalConfig:
  request_timeout: float
