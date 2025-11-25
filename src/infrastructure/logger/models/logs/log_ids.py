from dataclasses import dataclass


@dataclass
class LogIDs:
  correlation_id: str
  request_id: str
