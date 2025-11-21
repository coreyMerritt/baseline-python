from services.exceptions.service_exception import ServiceException


class BadInputErr(ServiceException):
  message: str

  def __init__(self, *args):
    message="Bad input."
    self.message = message
    super().__init__(message, *args)
