from infrastructure.exceptions.infrastructure_exception import BaseInfrastructureException


class LoggerConfigurationErr(BaseInfrastructureException):
  message: str

  def __init__(self, *args):
    message="Failed to configure logger."
    self.message = message
    super().__init__(message, *args)
