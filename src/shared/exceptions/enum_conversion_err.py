from shared.exceptions.base_shared_exception import BaseSharedException


class EnumConversionErr(BaseSharedException):
  message: str

  def __init__(self, string: str, *args):
    message=f"Failed to convert primitive to enum: {string}"
    self.message = message
    super().__init__(message, *args)
