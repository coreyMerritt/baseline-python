from interfaces.exceptions.interface_exception import InterfaceException


class UnknownCommandException(InterfaceException):
  message: str

  def __init__(self, *args):
    message="Unknown command."
    self.message = message
    super().__init__(message, *args)
