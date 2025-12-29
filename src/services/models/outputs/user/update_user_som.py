from dataclasses import dataclass


@dataclass
class UpdateUserSOM:
  ulid: str
  email_address: str
  username: str
