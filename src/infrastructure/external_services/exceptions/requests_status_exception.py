class RequestsStatusException(Exception):
  _status_code: int
  _reason: str

  def __init__(self, status_code: int, reason: str):
    if not isinstance(status_code, int):
      raise TypeError("status_code must be an int")
    if not isinstance(reason, str):
      raise TypeError("reason must be a str")

    self._status_code = status_code
    self._reason = reason
    super().__init__(f"HTTP {status_code}: {reason}")
