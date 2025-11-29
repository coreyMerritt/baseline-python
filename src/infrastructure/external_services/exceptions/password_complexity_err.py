from infrastructure.exceptions.infrastructure_exception import BaseInfrastructureException


class PasswordComplexityErr(BaseInfrastructureException):
  message: str

  def __init__(self, *args):
    message="Password does not meet complexity requirements."
    self.message = message
    super().__init__(message, *args)
