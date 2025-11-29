from dataclasses import dataclass


@dataclass
class GetUserSOM:
  uuid: str
  email_address: str
  username: str
