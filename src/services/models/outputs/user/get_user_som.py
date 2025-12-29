from dataclasses import dataclass


@dataclass
class GetUserSOM:
  ulid: str
  email_address: str
  username: str
