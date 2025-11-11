from infrastructure.abc_infrastructure import Infrastructure
from infrastructure.config.models.external_services_config import ExternalServicesConfig
from infrastructure.external_services.models.external_services_health_report import ExternalServicesHealthReport


class ExternalServiceManager(Infrastructure):
  _external_services_config: ExternalServicesConfig

  def __init__(self, external_services_config: ExternalServicesConfig):
    self._external_services_config = external_services_config

  def get_health_report(self) -> ExternalServicesHealthReport:
    is_external_services_config = self._external_services_config is not None
    healthy = is_external_services_config
    return ExternalServicesHealthReport(
      is_external_services_config=is_external_services_config,
      healthy=healthy
    )
