from infrastructure.exceptions.infrastructure_exception import InfrastructureException


class ZeroQueryResultsErr(InfrastructureException):
  message: str

  def __init__(self, *args):
    message="Query returned zero results."
    self.message = message
    super().__init__(message, *args)
