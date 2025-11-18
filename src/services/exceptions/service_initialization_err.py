from services.exceptions.service_exception import ServiceException


class ServiceInitializationErr(ServiceException):
  message: str

  def __init__(self, *args):
    message="Failed to initialize service."
    self.message = message
    super().__init__(message, *args)
