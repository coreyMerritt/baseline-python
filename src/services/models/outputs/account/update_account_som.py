from dataclasses import dataclass
from datetime import datetime

from domain.enums.account_status import AccountStatus


@dataclass
class UpdateAccountSOM:
  ulid: str
  name: str
  status: AccountStatus
  created_at: datetime
  suspended_at: datetime | None
  deleted_at: datetime | None
