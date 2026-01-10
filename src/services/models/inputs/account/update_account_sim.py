from dataclasses import dataclass

from domain.enums.account_status import AccountStatus


@dataclass(frozen=True)
class UpdateAccountSIM:
  ulid: str
  name: str
  status: AccountStatus
