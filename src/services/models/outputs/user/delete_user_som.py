from dataclasses import dataclass


@dataclass(frozen=True)
class DeleteUserSOM:
  ulid: str
  email_address: str
  username: str
