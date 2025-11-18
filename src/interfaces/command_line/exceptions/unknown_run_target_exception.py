class UnknownRunTargetException(Exception):
  message: str

  def __init__(self, *args):
    message="Unknown \"run\" target."
    self.message = message
    super().__init__(message, *args)
