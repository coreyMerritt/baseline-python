from services.exceptions.base_service_exception import BaseServiceException


class AccountDeletedErr(BaseServiceException):
  message: str

  def __init__(self, *args):
    message="Cannot perform action on a deleted account."
    self.message = message
    super().__init__(message, *args)
