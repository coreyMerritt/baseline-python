from interfaces.exceptions.interface_exception import InterfaceException


class RestAdapterErr(InterfaceException):
  message: str

  def __init__(self, *args):
    message="Rest adapter error occurred"
    self.message = message
    super().__init__(message, *args)
