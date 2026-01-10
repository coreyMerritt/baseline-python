from dataclasses import dataclass


@dataclass(frozen=True)
class UserCredential:
  user_ulid: str
  password_hash: str
