from services.exceptions.service_exception import ServiceException


class ItemNotFoundErr(ServiceException):
  message: str

  def __init__(self, *args):
    message="Failed to retrieve item."
    self.message = message
    super().__init__(message, *args)
