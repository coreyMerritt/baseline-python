from infrastructure.exceptions.infrastructure_exception import InfrastructureException


class LoggerLevelErr(InfrastructureException):
  message: str

  def __init__(self, *args):
    message="Failed to interpret logger level"
    self.message = message
    super().__init__(message, *args)
