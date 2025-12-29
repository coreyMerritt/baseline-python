from dataclasses import dataclass


@dataclass
class CreateUserSOM:
  ulid: str
  email_address: str
  username: str
