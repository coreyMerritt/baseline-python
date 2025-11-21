from dataclasses import dataclass

from domain.enums.account_type import AccountType


@dataclass
class CreateAccountSOM:
  uuid: str
  name: str
  age: int
  account_type: AccountType
