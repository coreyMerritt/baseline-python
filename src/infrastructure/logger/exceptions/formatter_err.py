from infrastructure.exceptions.infrastructure_exception import BaseInfrastructureException


class FormatterErr(BaseInfrastructureException):
  message: str

  def __init__(self, *args):
    message="Failed to format logs."
    self.message = message
    super().__init__(message, *args)
