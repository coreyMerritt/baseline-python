from infrastructure.exceptions.infrastructure_exception import InfrastructureException


class DiskReadErr(InfrastructureException):
  message: str

  def __init__(self, filename: str, *args):
    message=f"Failed to read file: {filename}"
    self.message = message
    super().__init__(message, *args)
