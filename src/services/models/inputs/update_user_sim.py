from dataclasses import dataclass


@dataclass
class UpdateUserSIM:
  uuid: str
  email_address: str | None
  username: str | None
  password: str | None
