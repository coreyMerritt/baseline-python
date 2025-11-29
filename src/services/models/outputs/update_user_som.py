from dataclasses import dataclass


@dataclass
class UpdateUserSOM:
  uuid: str
  email_address: str
  username: str
