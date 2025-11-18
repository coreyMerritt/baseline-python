from domain.exceptions.domain_exception import DomainException


class DomainMapperErr(DomainException):
  message: str

  def __init__(self, *args):
    message="Domain mapping error occurred"
    self.message = message
    super().__init__(message, *args)
