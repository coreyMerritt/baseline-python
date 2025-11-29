from dataclasses import dataclass


@dataclass
class DeleteUserSOM:
  uuid: str
  email_address: str
  username: str
