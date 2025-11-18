from infrastructure.exceptions.infrastructure_exception import InfrastructureException


class LoggerInitializationErr(InfrastructureException):
  message: str

  def __init__(self, *args):
    message="Failed to initialize logger."
    self.message = message
    super().__init__(message, *args)
