from services.exceptions.service_exception import ServiceException


class ItemCreationErr(ServiceException):
  message: str

  def __init__(self, *args):
    message="Failed to create item."
    self.message = message
    super().__init__(message, *args)
