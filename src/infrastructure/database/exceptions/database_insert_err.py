from infrastructure.exceptions.infrastructure_exception import InfrastructureException


class DatabaseInsertErr(InfrastructureException):
  message: str

  def __init__(self, *args):
    message="Failed to insert into database."
    self.message = message
    super().__init__(message, *args)
