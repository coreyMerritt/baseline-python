from dataclasses import dataclass


@dataclass
class CreateUserSIM:
  email_address: str
  username: str
  password: str
