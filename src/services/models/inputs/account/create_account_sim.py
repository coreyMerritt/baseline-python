from dataclasses import dataclass


@dataclass(frozen=True)
class CreateAccountSIM:
  name: str
