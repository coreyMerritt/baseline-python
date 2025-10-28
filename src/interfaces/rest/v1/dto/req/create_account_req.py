from pydantic import BaseModel


class CreateAccountReq(BaseModel):
  name: str
  age: int
  account_type: str
