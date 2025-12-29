from pydantic import BaseModel


class UpdateUserReq(BaseModel):
  ulid: str
  username: str
  email_address: str
  email_verified: bool
  disabled: bool
