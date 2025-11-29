from dataclasses import dataclass


@dataclass
class CreateUserSOM:
  uuid: str
  email_address: str
  username: str
