import re

from domain.exceptions.validation_err import ValidationErr


class EmailValidator:
  EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
  )

  @staticmethod
  def validate(email: str) -> None:
    if not isinstance(email, str):
      raise ValidationErr("email", "non-str")
    if not EmailValidator.EMAIL_REGEX.match(email):
      raise ValidationErr("email", "invalid format")
