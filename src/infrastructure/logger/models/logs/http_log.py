from dataclasses import dataclass

from infrastructure.logger.models.logs.base_log import BaseLog
from infrastructure.logger.models.logs.log_ids import LogIDs


@dataclass
class HTTPLog(BaseLog):
  ids: LogIDs
  endpoint: str
