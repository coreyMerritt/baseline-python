from dataclasses import dataclass


@dataclass(frozen=True)
class AuthenticatorConfig():
  secret: str
