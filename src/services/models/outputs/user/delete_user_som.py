from dataclasses import dataclass


@dataclass
class DeleteUserSOM:
  ulid: str
  email_address: str
  username: str
