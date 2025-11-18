from interfaces.exceptions.interface_exception import InterfaceException


class UnknownRunTargetException(InterfaceException):
  message: str

  def __init__(self, *args):
    message="Unknown \"run\" target."
    self.message = message
    super().__init__(message, *args)
