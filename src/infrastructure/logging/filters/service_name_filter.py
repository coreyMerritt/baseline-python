import logging


class ServiceNameFilter(logging.Filter):
  def __init__(self, service_name: str):
    super().__init__()
    self.service_name = service_name

  def filter(self, record: logging.LogRecord) -> bool:
    if not hasattr(record, 'service_name'):
      record.service_name = "Unknown"
    record.service_name = self.service_name
    return True
