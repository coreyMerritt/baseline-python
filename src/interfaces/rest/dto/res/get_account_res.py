from pydantic import BaseModel


class GetAccountRes(BaseModel):
  uuid: str
  name: str
  age: int
  account_type: str
