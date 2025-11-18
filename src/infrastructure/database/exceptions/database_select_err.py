from infrastructure.exceptions.infrastructure_exception import InfrastructureException


class DatabaseSelectErr(InfrastructureException):
  message: str

  def __init__(self, *args):
    message="Failed to select data from database."
    self.message = message
    super().__init__(message, *args)
