from infrastructure.exceptions.infrastructure_exception import InfrastructureException


class DatabaseMapperErr(InfrastructureException):
  message: str

  def __init__(self, *args):
    message="Database mapping error occurred"
    self.message = message
    super().__init__(message, *args)
