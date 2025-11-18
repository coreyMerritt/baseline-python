from interfaces.exceptions.interface_exception import InterfaceException


class AppInitializationErr(InterfaceException):
  message: str

  def __init__(self, *args):
    message="Failed to initialize Application."
    self.message = message
    super().__init__(message, *args)
