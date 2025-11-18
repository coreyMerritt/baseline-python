from infrastructure.exceptions.infrastructure_exception import InfrastructureException


class RequestsParseErr(InfrastructureException):
  message: str

  def __init__(self, *args):
    message="Failed to parse response from HTTP request."
    self.message = message
    super().__init__(message, *args)
