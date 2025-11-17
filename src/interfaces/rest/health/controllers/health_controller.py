import asyncio
from logging import Logger

from fastapi import Request

from interfaces.rest.exceptions.rest_adapter_err import RestAdapterErr
from interfaces.rest.exceptions.projectname_http_exception import ProjectnameHTTPException
from interfaces.rest.health.adapters.get_full_health_report_adapter import GetFullHealthReportAdapter
from interfaces.rest.models.projectname_http_response import ProjectnameHTTPResponse
from services.health_manager import HealthManager
from services.logger_passer import LoggerPasser


class HealthController:
  _req: Request
  _logger: Logger
  _health_manager: HealthManager

  def __init__(self, req: Request):
    self._req = req
    self._logger = LoggerPasser().get_logger()
    self._health_manager = HealthManager(req.app.state.db)

  # NOTE: Most GETs will not use a Req, just one or more query params /health?uuid=123
  async def get_full_health_report(self) -> ProjectnameHTTPResponse:
    try:
      health_report = await asyncio.to_thread(self._health_manager.get_full_health_report)
      self._logger.info("Successfully retrieved full health report")
      get_full_health_report_res = GetFullHealthReportAdapter.model_to_res(health_report)
      return ProjectnameHTTPResponse(
        data=get_full_health_report_res
      )
    except RestAdapterErr as e:
      # We drop exec_info=e for low-concern exceptions
      self._logger.warning("Bad request")
      # We give proper error codes when possible with "detail" matching the error code summary
      raise ProjectnameHTTPException(
        status_code=400,
        message="Bad request"
      ) from e
