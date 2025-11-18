from infrastructure.exceptions.infrastructure_exception import InfrastructureException


class DatabaseSchemaCreationErr(InfrastructureException):
  message: str

  def __init__(self, *args):
    message="Failed to create database schema."
    self.message = message
    super().__init__(message, *args)
