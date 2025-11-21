from dataclasses import dataclass

from domain.enums.account_type import AccountType


@dataclass
class CreateAccountSIM:
  uuid: str | None
  name: str
  age: int
  account_type: AccountType
