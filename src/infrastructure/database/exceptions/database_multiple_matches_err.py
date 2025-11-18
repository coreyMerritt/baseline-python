from infrastructure.exceptions.infrastructure_exception import InfrastructureException


class DatabaseMultipleMatchesErr(InfrastructureException):
  message: str

  def __init__(self, *args):
    message="Multiple matches found in a situation where only one match is expected."
    self.message = message
    super().__init__(message, *args)
