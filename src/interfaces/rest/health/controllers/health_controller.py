import asyncio
from logging import Logger

from fastapi import Request

from interfaces.rest.health.adapters.get_full_health_report_adapter import GetFullHealthReportAdapter
from interfaces.rest.models.projectname_http_response import ProjectnameHTTPResponse
from services.health_manager import HealthManager
from shared.models.configs.external_services.external_services_config import ExternalServicesConfig
from shared.models.configs.health_check_config import HealthCheckConfig


class HealthController:
  _req: Request
  _logger: Logger
  _external_services_config: ExternalServicesConfig
  _health_check_config: HealthCheckConfig
  _health_manager: HealthManager

  def __init__(self, req: Request):
    self._req = req
    self._logger = req.app.state.logger
    self._external_services_config = req.app.state.config.external_services
    self._health_check_config = req.app.state.config.health_check
    self._health_manager = HealthManager(req.app.state.database)

  # NOTE: Most GETs will not use a Req, just one or more query params /health?uuid=123
  async def get_full_health_report(self) -> ProjectnameHTTPResponse:
    health_report = await asyncio.to_thread(
      self._health_manager.get_full_health_report,
      self._external_services_config,
      self._health_check_config
    )
    self._logger.info("Successfully retrieved full health report")
    get_full_health_report_res = GetFullHealthReportAdapter.model_to_res(health_report)
    return ProjectnameHTTPResponse(
      data=get_full_health_report_res
    )
