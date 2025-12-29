from pydantic import BaseModel


class CreateAccountReq(BaseModel):
  name: str
