from infrastructure.exceptions.infrastructure_exception import InfrastructureException


class LoggerConfigurationErr(InfrastructureException):
  message: str

  def __init__(self, *args):
    message="Failed to configure logger."
    self.message = message
    super().__init__(message, *args)
