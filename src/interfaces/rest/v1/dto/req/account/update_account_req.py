from pydantic import BaseModel

from domain.enums.account_status import AccountStatus


class UpdateAccountReq(BaseModel):
  ulid: str
  name: str
  status: AccountStatus
