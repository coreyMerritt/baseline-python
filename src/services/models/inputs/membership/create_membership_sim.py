from dataclasses import dataclass


@dataclass
class CreateMembershipSIM:
  user_ulid: str
  account_ulid: str
  role_ulid: str
