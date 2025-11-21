from services.exceptions.service_exception import ServiceException


class ServiceUnavailableErr(ServiceException):
  message: str

  def __init__(self, *args):
    message="Service unavailable."
    self.message = message
    super().__init__(message, *args)
