from services.exceptions.service_exception import ServiceException


class ServiceMapperErr(ServiceException):
  message: str

  def __init__(self, *args):
    message="Service mapping error occurred"
    self.message = message
    super().__init__(message, *args)
