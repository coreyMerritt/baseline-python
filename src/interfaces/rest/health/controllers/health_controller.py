import asyncio
from logging import Logger

from fastapi import HTTPException

from infrastructure.logging.log_manager import LogManager
from interfaces.rest.health.adapters.get_full_health_report_adapter import GetFullHealthReportAdapter
from interfaces.rest.health.dto.res.get_full_health_report_res import GetFullHealthReportRes
from interfaces.rest.health.exceptions.health_adapter_exception import HealthAdapterException
from services.health_manager import HealthManager


class HealthController:
  _logger: Logger
  _health_manager: HealthManager

  def __init__(self):
    self._logger = LogManager.get_logger(self.__class__.__name__)
    self._health_manager = HealthManager()

  # NOTE: Most GETs will not use a Req, just one or more query params /health?uuid=123
  async def get_full_health_report(self) -> GetFullHealthReportRes:
    try:
      health_report = await asyncio.to_thread(self._health_manager.get_full_health_report)
      self._logger.info("Successfully retrieved full health report")
      return GetFullHealthReportAdapter.valueobject_to_res(health_report)
    except HealthAdapterException as e:
      # We drop exec_info=e for low-concern exceptions
      self._logger.warning("Bad request")
      # We give proper error codes when possible with "detail" matching the error code summary
      raise HTTPException(status_code=400, detail="Bad request") from e
    except Exception as e:
      self._logger.error("Unknown exception -- Failed to get full health report", exc_info=e)
      raise HTTPException(status_code=500, detail="Internal server error") from e
